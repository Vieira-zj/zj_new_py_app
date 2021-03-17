# -*- coding: utf-8 -*-
'''
Created on 2019-01-30
@author: zhengjin
'''

import random
import os


def generate_data_from_csv(count):
    root_dir = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files/prophet_testdata')
    input_file_path = os.path.join(root_dir, 'test_data.csv')
    if not os.path.exists(input_file_path):
        print('input file NOT exist:', input_file_path)
        exit(1)

    # read src data
    input_lines = []
    with open(input_file_path, mode='r', encoding='utf-8') as f:
        input_lines = f.readlines()
    print('total input lines:', len(input_lines))

    # generate data
    output_file_path = os.path.join(root_dir, 'test_data_out.csv')
    with open(output_file_path, mode='w', encoding='utf-8') as f:
        f.writelines([input_lines[0]])  # first line as schema

        for line in input_lines[1:]:
            output_lines = [line]
            for i in range(0, count):
                fields = line.split(',')
                fields[0] = str(random.randint(0, 100))
                fields[12] = str(random.randint(0, 1000))
                output_lines.append(','.join(fields))
            f.writelines(output_lines)

    print('generate csv data done.')


if __name__ == '__main__':

    generate_data_from_csv(10)
