# -*- coding: utf-8 -*-
'''
Created on 2018-11-20

@author: zhengjin
'''

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.getenv('PYPATH'))
from utils import Constants, LogManager, SysUtils


class ChartParser(object):
    '''
    Generate profile chart include CPU, Memory (Pss), Upflow, Downflow.
    '''

    CATEGORY_CPU = 0
    CATEGORY_MEM = 1
    CATEGORY_UPFLOW = 2
    CATEGORY_DOWNFLOW = 3

    __profile_types_list = ('cpu_com_jd_b2b.txt,cpuSystem.txt',
                            'pss_com_jd_b2b.txt,pssSystemLeft.txt',
                            'upflow_com_jd_b2b.txt',
                            'downflow_com_jd_b2b.txt')

    def __init__(self, report_root_path):
        '''
        Constructor
        '''
        self.__logger = LogManager.get_logger()
        self.__report_root_path = report_root_path
        self.__handtest_dir_path = os.path.join(self.__report_root_path, 'handTest')
        self.sysutils = SysUtils()
        
    # --------------------------------------------------------------
    # Read Profile Source Data
    # --------------------------------------------------------------
    def __read_profile_data(self, profile_types):
        if len(profile_types) > 2:
            raise Exception('Invalid number of profile types!')

        y1_arr = self.sysutils.read_lines_from_file(
            self.__get_abs_profile_filepath(profile_types[0]))
        if len(y1_arr) == 0:
            raise Exception('y1_arr length is zero!')

        y2_arr = []
        if len(profile_types) == 2:
            y2_arr = self.sysutils.read_lines_from_file(
                self.__get_abs_profile_filepath(profile_types[1]))

        ret_y1_arr = [int(float(item.split()[1])) for item in y1_arr]
        ret_y2_arr = []
        if len(y2_arr) > 0:
            ret_y2_arr = [int(float(item.split()[1])) for item in y2_arr]

        return self.__fix_negative_num_issue(ret_y1_arr), self.__fix_negative_num_issue(ret_y2_arr)

    def __get_abs_profile_filepath(self, file_name):
        return os.path.join(self.__handtest_dir_path, file_name)

    def __fix_negative_num_issue(self, y_arr):
        for i in range(0, len(y_arr)):
            if y_arr[i] < 0:
                y_arr[i] = 0
        return y_arr

    # --------------------------------------------------------------
    # Build Charts
    # --------------------------------------------------------------
    def build_all_profile_charts(self):
        self.build_profile_chart(ChartParser.CATEGORY_CPU)
        self.build_profile_chart(ChartParser.CATEGORY_MEM)
        self.build_profile_chart(ChartParser.CATEGORY_UPFLOW)
        self.build_profile_chart(ChartParser.CATEGORY_DOWNFLOW)

    def build_profile_chart(self, p_category, is_show=False):
        plt.title('APP Profile Test')
        plt.grid(True, color='green', linestyle='--', linewidth='1')

        profile_types = self.__profile_types_list[p_category].split(',')
        if p_category == self.CATEGORY_CPU:
            self.__build_cpu_chart(profile_types)
            self.__save_profile_image('cpu')
        elif p_category == self.CATEGORY_MEM:
            self.__build_mem_pss_chart(profile_types)
            self.__save_profile_image('mem')
        elif p_category == self.CATEGORY_UPFLOW:
            self.__build_upflow_chart(profile_types)
            self.__save_profile_image('upflow')
        elif p_category == self.CATEGORY_DOWNFLOW:
            self.__build_downflow_chart(profile_types)
            self.__save_profile_image('downflow')
        else:
            raise Exception('Invalid input profile category!')

        if is_show:
            plt.show()
        plt.close('all')

    def __build_cpu_chart(self, profile_types):
        y1_arr, y2_arr = self.__read_profile_data(profile_types)
        x_arr = [x for x in range(0, len(y1_arr))]
        plt.plot(x_arr, y1_arr, color='red')
        plt.plot(x_arr, y2_arr, color='blue')

        x_label_desc1 = 'Red: %s (average: %.2f%%, max: %d%%)' \
            % (profile_types[0].rstrip('.txt'), np.average(y1_arr), np.max(y1_arr))
        x_label_desc2 = 'Blue: %s (average: %.2f%%, max: %d%%)' \
            % (profile_types[1].rstrip('.txt'), np.average(y2_arr), np.max(y2_arr))
        plt.xlabel('Time (secs)\n%s\n%s' % (x_label_desc1, x_label_desc2))
        plt.ylabel('CPU usage (%)')

    def __build_mem_pss_chart(self, profile_types):
        y1_arr, y2_arr = self.__read_profile_data(profile_types)
        x_arr = [x for x in range(0, len(y1_arr))]
        plt.plot(x_arr, y1_arr, color='red')
        plt.plot(x_arr, y2_arr, color='blue')

        x_label_desc1 = 'Red: %s (average: %.2f MB, max: %d MB)' \
            % (profile_types[0].rstrip('.txt'), np.average(y1_arr), np.max(y1_arr))
        x_label_desc2 = 'Blue: %s (average: %.2f MB, max: %d MB)' \
            % (profile_types[1].rstrip('.txt'), np.average(y2_arr), np.max(y2_arr))
        plt.xlabel('Time (secs)\n%s\n%s' % (x_label_desc1, x_label_desc2))
        plt.ylabel('Memory Pss Usage (MB)')

    def __build_upflow_chart(self, profile_types):
        y_arr, _ = self.__read_profile_data(profile_types)
        x_arr = [x for x in range(0, len(y_arr))]
        plt.plot(x_arr, y_arr, color='red')

        x_label_desc = 'Red: ' + profile_types[0].rstrip('.txt')
        plt.xlabel('Time (secs)\n%s' % x_label_desc)
        plt.ylabel('Upflow (KB)')

    def __build_downflow_chart(self, profile_types):
        y_arr, _ = self.__read_profile_data(profile_types)
        x_arr = [x for x in range(0, len(y_arr))]
        plt.plot(x_arr, y_arr, color='red')

        x_label_desc = 'Red: ' + profile_types[0].rstrip('.txt')
        plt.xlabel('Time (secs)\n%s' % x_label_desc)
        plt.ylabel('Downflow (KB)')

    def __save_profile_image(self, key):
        save_dpi = 300
        save_path = os.path.join(self.__report_root_path, 'profile_%s.png' % key)
        plt.tight_layout()
        plt.savefig(save_path, format='png', dpi=save_dpi)


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)

    root_path = '/Users/zhengjin/Downloads/tmp_files'
    parser = ChartParser(root_path)
#     parser.build_all_profile_charts()
    parser.build_profile_chart(ChartParser.CATEGORY_CPU, True)
#     parser.build_profile_chart(ChartParser.CATEGORY_MEM, True)
#     parser.build_profile_chart(ChartParser.CATEGORY_UPFLOW)
#     parser.build_profile_chart(ChartParser.CATEGORY_DOWNFLOW, True)

    LogManager.clear_log_handles()
    print('chart parser test DONE.')
