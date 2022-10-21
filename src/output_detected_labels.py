#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import yaml
import wordnet_jp
import glob
import csv
import numpy as np

from __init__ import *

def has_duplicates(seq):
    return len(seq) != len(set(seq))


data_path = '../data/finish_tmp/'
files = len(glob.glob1("../data/finish_tmp/", "*_Object_BOO.csv"))

# with open('./yolo9000.yaml', 'r') as yml:
#     config = yaml.load(yml)
#
# object_dictionary = config['yolo_model']['detection_classes']['names']
# print("YOLO9000のラベル数：{}".format(len(object_dictionary))) # yolo9000のラベル数は9418

sum = 0
for k in range(files):
    boo_data = []
    with open(data_path + "{}_Object_BOO.csv".format(k + 1)) as f:
        reader = csv.reader(f)
        for row in reader:
            boo_data.append(row)

    # 型変換
    for i in range(len(boo_data[0])):
        boo_data[0][i] = int(boo_data[0][i])
    boo = np.array(boo_data[0])
    # print(boo_data)

    sum += boo
sum_list = sum.tolist()
# print(sum_list)


sum_list_big_index = [i for i, x in enumerate(sum_list) if x > 0] # 0以上の要素を持つindexを抽出
# print(sum_list_big_index)
# 対応するyoloのラベルの抽出
yolo_big_label = []
for k in range(len(sum_list_big_index)):
    yolo_big_label.append(object_dictionary[sum_list_big_index[k]])
print(yolo_big_label)


sum_list_big = [i for i in sum if i > 0]
print(sum_list_big)
sum_list_sort = sorted(sum_list_big)
flag = has_duplicates(sum_list_sort)

if flag is True:
    yolo_big_index_one = []
    yolo_big_index_two = []
    yolo_big_index_three = []
    for j in range(3):
        sum_list_sort = sorted(sum_list_big)
        if sum_list_sort.count(sum_list_sort[-1 * (j  + 1)]) > 1:
            value = sum_list_sort[-1 * (j  + 1)]
            index = [i for i, x in enumerate(sum_list) if x == value]
            for i in range(len(index)):
                if j + 1 == 1:
                    yolo_big_index_one.append(object_dictionary[index[i]])
                elif j + 1 == 2:
                    yolo_big_index_two.append(object_dictionary[index[i]])
                elif j + 1 == 3:
                    yolo_big_index_three.append(object_dictionary[index[i]])
        else:
            sum_list_sort = sorted(sum_list_big)[-1 * (j  + 1)]
            if j + 1 == 1:
                yolo_big_index_one = object_dictionary[sum_list.index(sum_list_sort)]
            elif j + 1 == 2:
                yolo_big_index_two = object_dictionary[sum_list.index(sum_list_sort)]
            elif j + 1 == 3:
                yolo_big_index_three = object_dictionary[sum_list.index(sum_list_sort)]
    print("1: {}, 2: {}, 3: {}".format(yolo_big_index_one, yolo_big_index_two, yolo_big_index_three))

else:
    try:
        yolo_big_index_one = object_dictionary[sum_list.index(sum_list_sort[-1])]
    except IndexError:
        yolo_big_index_one = []

    try:
        yolo_big_index_two = object_dictionary[sum_list.index(sum_list_sort[-2])]
    except IndexError:
        yolo_big_index_two = []

    try:
        yolo_big_index_three = object_dictionary[sum_list.index(sum_list_sort[-3])]
    except IndexError:
        yolo_big_index_three = []

    print("1: {}, 2: {}, 3: {}".format(yolo_big_index_one, yolo_big_index_two, yolo_big_index_three))




