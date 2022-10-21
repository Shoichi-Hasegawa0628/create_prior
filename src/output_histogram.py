#! /usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import numpy as np
import glob
from matplotlib import pyplot as plt

from __init__ import *

data_path = '../data/tmp_boo/'
# result_path = '../data/graph/living/'
# result_path = '../data/graph/kitchen/'
# result_path = '../data/graph/bathroom/'
# result_path = '../data/graph/bedroom/'

files = len(glob.glob1("../data/tmp_boo/", "*_Object_BOO.csv"))
print(files)

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

print(sum)

x = list(range(len(object_dictionary)))

# グラフの描画
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.plot(x, sum)
ax.set_xlim(1, len(object_dictionary))

plt.xlabel("Object label index")
plt.ylabel("The frequency of detected objects")
ax.set_ylim(0, 300)

# plt.show()
list_file = ["png", "pdf", "svg", "eps"]

for i in range(len(list_file)):
    # fig.savefig("/root/HSR/frequency/living/living_hist_yolov5_ISRD.{}".format(list_file[i]))
    # fig.savefig("/root/HSR/frequency/kitchen/kitchen_hist_yolov5_ISRD.{}".format(list_file[i]))
    # fig.savefig("/root/HSR/frequency/bathroom/bathroom_hist_yolov5_ISRD.{}".format(list_file[i]))
    fig.savefig("/root/HSR/frequency/bedroom/bedroom_hist_yolov5_ISRD.{}".format(list_file[i]))

# fig.savefig("/root/HSR/frequency/living/living_hist_yolo9000_ISRD.png")
# fig.savefig("/root/HSR/frequency/living/living_hist_yolo9000_ISRD.pdf")
# fig.savefig("/root/HSR/frequency/living/living_hist_yolo9000_ISRD.svg")
# fig.savefig("/root/HSR/frequency/living/living_hist_yolo9000_ISRD.eps")
