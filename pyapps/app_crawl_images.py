# -*- coding: utf-8 -*-
'''
Created on 2019-05-20
@author: zhengjin
'''

import logging
import os
import re
import sys
sys.path.append(os.getenv('PYPATH'))

from appdemos import CrawlHtml
from utils import Constants, LogManager, HttpUtils, SysUtils


class CrawlImages(object):

    def __init__(self):
        self._logger = LogManager.get_logger()

    def crawl_pages_count(self, url):
        last_page = CrawlHtml.get_instance().fetch_html_content(url) \
            .get_ui_element_by_css('.pagelist a:last')
        results = re.match('list_[0-9]_([0-9]+).html', last_page.attr('href'))
        return results.group(1)

    def crawl_article_links_of_page(self, url):
        links = CrawlHtml.get_instance().fetch_html_content(url) \
            .get_ui_element_by_css('.text1_1text .list a').items()
        return [link.attr('href') for link in links]

    def crawl_page_images_process(self, url):
        self._logger.info('crawl images for page: ' + url)
        img_urls = self._crawl_image_urls_of_page(url)
        if len(img_urls) == 0:
            return

        res = re.search('([0-9]+).html$', url)
        dir_name = '%s_%d' % (res.group(1), len(img_urls))
        save_dir_path = os.path.join(
            os.getenv('HOME'), 'Downloads/tmp_files/crawl_images', dir_name)
        if not os.path.exists(save_dir_path):
            os.makedirs(save_dir_path)

        for url in img_urls:
            self._download_and_save_images(url, save_dir_path)

    def _crawl_image_urls_of_page(self, url):
        images = CrawlHtml.get_instance().fetch_html_content(url) \
            .get_ui_element_by_css('.centen2 img').items()
        base_url = 'http://www.522yw.city'
        return [base_url + img.attr('src') for img in images]

    def _download_and_save_images(self, url, save_dir_path):
        items = url.split('/')
        file_name = items[len(items) - 1]
        save_path = os.path.join(save_dir_path, file_name)

        if os.path.exists(save_path):
            return
        CrawlHtml.get_instance().get_and_save_files(url, save_path)

    def crawl_images_main(self):
        from concurrent.futures import ProcessPoolExecutor
        from concurrent.futures import wait

        def _fn_page_filter(i):
            return i == 6
            # return i >= 3 and i < 6

        home_url = 'http://www.522yw.city/article/list_3.html'
        count = self.crawl_pages_count(home_url)

        page_urls = []
        base_url = 'http://www.522yw.city/article/list_3_%d.html'
        # page_urls.append(home_url)
        page_urls.extend([base_url % i for i in range(1, int(count)) if _fn_page_filter(i)])

        f_submit = []
        executor = ProcessPoolExecutor(max_workers=3)
        for page_url in page_urls:
            article_urls = self.crawl_article_links_of_page(page_url)
            f_submit.extend(
                [executor.submit(self.crawl_page_images_process, url) for url in article_urls])
        f_done = wait(f_submit, return_when='ALL_COMPLETED')

        self._logger.info('\n\nSUMMARY:')
        self._logger.info('number of %d tasks (task => article) done.' % len(f_done.done))
        self._logger.info('FAILED tasks:')
        for future in f_done.done:
            if future.exception() is not None:
                self._logger.error(str(future.exception()))


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)
    CrawlImages().crawl_images_main()
    LogManager.clear_log_handles()
    print('crawl images demo DONE!')
