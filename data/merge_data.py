# -*- coding: utf-8 -*-
# Author: 薄荷你玩
# Date: 2023/05/12
import os


def merge_data(path='normal'):
    normal_file = open('normal.txt', 'a+', encoding='utf8')
    spam_file = open('spam.txt', 'a+', encoding='utf8')

    for file in os.listdir(path):
        is_spam = 'spam' in file
        with open(path + '/' + file, encoding='utf-8') as fi:
            lines = fi.readlines()
            if is_spam:
                spam_file.writelines(lines)
            else:
                normal_file.writelines(lines)
        print(file, is_spam, 'over')

merge_data('spam')
