# -*- coding: utf-8 -*-
'''
Created on 2019-05-20
@author: zhengjin

condition:
$ pip3 install pyquery
'''

import os
import sys
from pyquery import PyQuery as pq

sys.path.append(os.getenv('PYPROJECT'))
from utils import Constants
from utils import HttpUtils
from utils import LogManager


class CrawlHtml(object):

    _crawl = None

    @classmethod
    def get_instance(cls):
        if cls._crawl is None:
            cls._crawl = CrawlHtml()
        return cls._crawl

    def __init__(self):
        self.html_dom = None  # pq object for page html dom

    def fetch_html_content(self, url, query='', method=HttpUtils.HTTP_METHOD_GET, timeout=5):
        http_utils = HttpUtils.get_instance()
        resp = http_utils.send_http_request(method, url, query, timeout=timeout)
        try:
            self.html_dom = pq(resp.content.decode(encoding='utf-8'))
        except UnicodeDecodeError as _:
            self.html_dom = pq(resp.content.decode(encoding='gbk'))
        return self

    def get_ui_element_by_css(self, selector):
        if self.html_dom is None:
            raise Exception('Pls invoke fetch_html_content() before get ui elements.')
        return self.html_dom(selector)

    def get_and_save_files(self, url, save_path, query='', method=HttpUtils.HTTP_METHOD_GET, timeout=5):
        http_utils = HttpUtils.get_instance()
        resp = http_utils.send_http_request(method, url, query, timeout=timeout, is_log_body=False)

        with open(save_path, 'wb') as f:
            f.write(resp.content)
# end CrawlHtml


class CrawlText(object):

    def __init__(self):
        self._logger = LogManager.get_logger()

    def crawl_pages_count(self, url):
        pages_eles = CrawlHtml.get_instance().fetch_html_content(url, 'page=1') \
            .get_ui_element_by_css('.pagination>li>a').items()
        pages_list = [ele for ele in pages_eles]
        return pages_list[len(pages_list) - 2].text()

    def crawl_article_titles_of_page(self, url, query):
        selector = '.panel-body.item-list>div .title.media-heading>a'
        html_dom = CrawlHtml.get_instance().fetch_html_content(url, query)
        title_eles = html_dom.get_ui_element_by_css(selector).items()
        category_eles = html_dom.get_ui_element_by_css(selector + '>span').items()

        titles = []
        for item in zip(category_eles, title_eles):
            titles.append('Category: %s, Title: %s' % (item[0].text(), item[1].attr('title')))
        return titles

    def crawl_text_main(self):
        from concurrent.futures import ProcessPoolExecutor
        from concurrent.futures import wait

        url = 'https://testerhome.com/topics'
        count = self.crawl_pages_count(url)

        executor = ProcessPoolExecutor(max_workers=3)
        page_numbers = [i for i in range(0, int(count)) if i % 10 == 0]
        fs_submit = [executor.submit(self.crawl_article_titles_of_page, url, 'page=%d' % num)
                     for num in page_numbers]
        fs_finish = wait(fs_submit, return_when='ALL_COMPLETED')

        all_titles = []
        for f in fs_finish.done:
            all_titles.extend(f.result())

        self._logger.info('TESTING ARTICLE TITLES:')
        for titles in all_titles:
            self._logger.info(titles)


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)
    CrawlText().crawl_text_main()
    LogManager.clear_log_handles()
    print('crawl text (article titles) demo DONE!')
