#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library
from __future__ import unicode_literals
import codecs
import cv2
from cv_bridge import CvBridge, CvBridgeError
import os
import csv
import time

# Third Party
import numpy as np
import rospy
import message_filter
from sensor_msgs.msg import CompressedImage

# Self Modules
from __init__ import *

path = "/root/HSR/catkin_ws/src/create_prior/data/output"


class ObjectFeatureServer():
    def __init__(self):
        self.detect_object_info = []
        self.object_list = []
        self.Object_BOO = []
        self.cv_bridge = CvBridge()
        self.frame = 0
        self.file_index = 1
        self.img_pub = rospy.Publisher("/hsrb/head_rgbd_sensor/rgb/image_rect_color/compressed", CompressedImage)
        self.index_pub = rospy.Publisher("/file_index", String)
        rospy.loginfo("[Service spco_data/object] Ready")

        files = os.listdir("../data/image")
        for i in range(len(files)):
            self.frame = cv2.imread("../data/image/{}.jpg".format(i + 1))
            raw_img = self.cv_bridge.cv2_to_compressed_imgmsg(self.frame)
            self.object_server(i + 1, raw_img)

    def object_server(self, step, image):
        if (os.path.exists("../data/tmp_boo/Object.csv") == True):
            with open("../data/tmp_boo/Object.csv", 'r') as f:
                reader = csv.reader(f)
                self.object_list = [row for row in reader]
            # print("pre_object_list: {}\n".format(self.object_list))

        timeout = time.time() + 10
        while True:
            self.index_pub.publish(self.file_index)
            if time.time() > timeout:
                break

        timeout = time.time() + 30
        while True:
            self.img_pub.publish(image)
            if time.time() > timeout:
                break

        time.sleep(10)

        self.read_data(step)
        self.file_index += 1
        return

    def extracting_label(self):
        object_list = []
        for i in range(len(self.detect_object_info)):
            object_list.append(self.detect_object_info[i].Class)
            # print(object_list)
        self.object_list.append(object_list)
        # print(self.object_list)
        return

    def make_object_boo(self):
        # print(self.object_list)
        self.Object_BOO = [[0 for i in range(len(object_dictionary))] for n in range(len(self.object_list))]
        # print(self.Object_BOO)
        for n in range(len(self.object_list)):
            for j in range(len(self.object_list[n])):
                for i in range(len(object_dictionary)):
                    if object_dictionary[i] == self.object_list[n][j]:
                        self.Object_BOO[n][i] = self.Object_BOO[n][i] + 1
        # print(self.Object_BOO)
        return

    def save_data(self, step):
        # 全時刻の観測された物体のリストを保存
        FilePath = "../data/tmp_boo/Object.csv"
        with open(FilePath, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.object_list)

        # 教示ごとに観測された物体のリストを保存
        FilePath = "../data/tmp_boo/" + str(step) + "_Object.csv"
        with open(FilePath, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.object_list)

        # 教示ごとのBag-Of-Objects特徴量を保存
        FilePath = "../data/tmp_boo/" + str(step) + "_Object_BOO.csv"
        with open(FilePath, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.Object_BOO)

        # 教示ごとの物体の辞書を保存
        FilePath = "../data/tmp_boo/" + str(step) + "_Object_W_list.csv"
        with open(FilePath, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(object_dictionary)

        return

    def read_data(self, step):
        if ((os.path.exists(path + "/{}.jpg".format(self.file_index)) != True) and (
                os.path.exists(path + "/{}.csv".format(self.file_index)) != True)):
            if step == 1:
                # 最初の教示で物体が検出されなかったとき
                self.object_list = [[]]
                self.Object_BOO = [[0] * len(object_dictionary)]
                self.save_data(step)
                print("No object at the first step.")
                return

            else:
                # 最初の教示以降の教示で物体が検出されなかったとき
                object_list = []
                self.object_list.append(object_list)
                self.make_object_boo()
                self.save_data(step)
                print("No object")
                return

        with open(path + "/{}.csv".format(self.file_index), 'r') as f:
            reader = csv.reader(f)
            self.detect_object_info = [row for row in reader]

        self.extracting_label()
        self.make_object_boo()
        self.save_data(step)
        return


if __name__ == '__main__':
    rospy.init_node('create_prior', anonymous=False)
    srv = ObjectFeatureServer()
    rospy.spin()
