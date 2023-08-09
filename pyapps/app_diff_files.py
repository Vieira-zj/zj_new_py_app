# coding: utf-8

import difflib


def read_file_lines(file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        return f.readlines()


def print_diff_count(diff_results: str):
    count = 0
    count += diff_results.count('<span class="diff_sub">')
    count += int(diff_results.count('<span class="diff_chg">') / 2)
    count += diff_results.count('<span class="diff_add">')
    print('diff count:', count)


def diff_files(file1_path, file2_path, output_html_file_path):
    file1_lines = read_file_lines(file1_path)
    file2_lines = read_file_lines(file2_path)
    d = difflib.HtmlDiff()
    results = d.make_file(file1_lines, file2_lines)
    print_diff_count(results)

    with open(output_html_file_path, 'w',  encoding='utf8') as f:
        f.write(results)


if __name__ == '__main__':

    path1 = '/tmp/test/test1.json'
    path2 = '/tmp/test/test2.json'
    output_path = '/tmp/test/diff.html'
    diff_files(path1, path2, output_path)
    print('diff files done.')
