# -*- coding: utf-8 -*-
'''
Created on 2019-03-07
@author: zhengjin
'''

import os
import sys
import glob
import smtplib
import zipfile

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.path.index(project_dir)
except ValueError:
    sys.path.append(project_dir)

from utils import Constants
from utils import LogManager
from utils import SysUtils
Constants.add_project_paths()

from common import LoadConfigs


class EmailHelper(object):

    __email = None

    @classmethod
    def get_intance(cls):
        if cls.__email is None:
            cls.__email = EmailHelper()
        return cls.__email

    def __init__(self):
        self.__logger = LogManager.get_logger()
        self.__sysutils = SysUtils.get_instance()
        self.__configs = LoadConfigs.get_email_configs()

        self.__msg = MIMEMultipart('mixed')
        self.__content_text = 'Default mail template from API test.'

    # --------------------------------------------------------------
    # Build mail
    # --------------------------------------------------------------
    def __build_mail_header(self):
        receivers = self.__configs.get('receivers').split(',')

        self.__msg['subject'] = self.__configs.get('subject')
        self.__msg['from'] = self.__configs.get('sender')
        self.__msg['to'] = ';'.join(receivers)
        self.__msg['date'] = self.__sysutils.get_current_date_with_sep()

    def __build_mail_content(self):
        content_plain = MIMEText(self.__content_text, 'plain', 'utf-8')
        self.__msg.attach(content_plain)

    def __attach_archive_file(self, attach_path):
        self.__logger.info('mail attach file: ' + attach_path)
        archive = MIMEText(open(attach_path, 'rb').read(), 'base64', 'utf-8')
        archive['Content-Type'] = 'application/octet-stream'
        archive['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(attach_path)
        self.__msg.attach(archive)

    def set_content_text(self, text):
        self.__content_text = text
        return self

    # --------------------------------------------------------------
    # Send mail
    # --------------------------------------------------------------
    def send_email(self):
        self.__build_mail_header()
        self.__build_mail_content()

        dir_path = self.__get_output_dir()
        attach_path = self.__zip_files(dir_path)
        self.__attach_archive_file(attach_path)

        smtp = self.__create_smtp()
        from_addr = self.__configs.get('sender')
        to_addr = self.__configs.get('receivers').split(',')
        try:
            smtp.sendmail(from_addr, to_addr, self.__msg.as_string())
        finally:
            if smtp is not None:
                smtp.quit()

        self.__logger.info('Test results email has been send.')

    def __create_smtp(self):
        smtp = smtplib.SMTP()
        smtp.connect(self.__configs.get('mail_host'))
        smtp.login(self.__configs.get('mail_user'), self.__configs.get('mail_pwd'))
        return smtp

    def __zip_files(self, dir_path):
        if len(dir_path) == 0:
            self.__logger.error("skip zip files step!")
            return

        zip_file_name = 'test_results_%s.zip' % self.__sysutils.get_current_date_and_time()
        # NOTE: use a tmp dir for .zip file
        output_zip_path = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files', zip_file_name)
        zip_stream = zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED)
        try:
            for dir_path, subpaths, files in os.walk(dir_path):
                for file in files:
                    tmp_file = os.path.join(dir_path, file)
                    arc_name = tmp_file[tmp_file.index('output'):]
                    zip_stream.write(tmp_file, arcname=arc_name)
        finally:
            if zip_stream is not None:
                zip_stream.close()

        return output_zip_path

    def __get_output_dir(self):
        '''
        Get output dir path for test results.
        '''
        project_path = os.path.join(os.getenv('PYPATH'), 'apitest')
        output_dir_path = LoadConfigs.get_testenv_configs().get('output_dir')
        output_dir_path = output_dir_path.replace('{project}', project_path)

        if not os.path.exists(output_dir_path):
            self.__logger.error('test output dir is not exist: ' + output_dir_path)
            return ''
        if not os.path.isdir(output_dir_path):
            self.__logger.error('invalid test out dir: ' + output_dir_path)
            return ''
        return output_dir_path


if __name__ == '__main__':

    isTest = True

    if isTest:
        print('Done')
    else:
        # init logger and configs
        LogManager.build_logger(Constants.LOG_FILE_PATH)
        cfg_file_path = os.path.join(
            os.getenv('PYPATH'), 'apitest', 'configs.ini')
        LoadConfigs.load_configs(cfg_file_path)

        mail_content = 'API test done.\nPlease read details of results in attachment.'
        mail = EmailHelper.get_intance()
        mail.set_content_text(mail_content).send_email()

        LogManager.clear_log_handles()
        print('email helper test DONE.')
