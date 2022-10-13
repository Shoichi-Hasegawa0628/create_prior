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

# Third Party Library
import numpy as np
from tqdm import tqdm

# ROS Library
import rospy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String

# Self Modules
from __init__ import *

path = "/root/HSR/catkin_ws/src/create_prior/data/output"
yolo_width = 640
yolo_height = 640

class ObjectFeatureServer():
    def __init__(self):
        self.detect_object_info = []
        self.object_list = []
        self.Object_BOO = []
        self.cv_bridge = CvBridge()
        self.frame = 0
        self.file_index = 0
        self.img_pub = rospy.Publisher("/hsrb/head_rgbd_sensor/rgb/image_rect_color/compressed", CompressedImage, queue_size=1)
        self.index_pub = rospy.Publisher("/file_index", String, queue_size=1)
        rospy.loginfo("[Service spco_data/object] Ready")

        files = os.listdir("../data/image")
        for i in tqdm(range(len(files))):
            self.frame = cv2.imread("../data/image/{}.jpg".format(i + 1))

            # yolov5の入力画像サイズに収まるようにリサイズ
            img_height, img_width, channels = self.frame.shape[:3]
            if img_width > yolo_width or img_height > yolo_height:
                dst = self.scale_box(self.frame, 640, 640)
                print(f"{self.frame.shape} -> {dst.shape}")
                self.frame = dst
                img_height, img_width, channels = self.frame.shape[:3]
                # print("dst_width: " + str(img_width))
                # print("dst_height: " + str(img_height))

            # 640×640に合うように黒でパディング
            diff_height = 0
            diff_width = 0
            if img_height != 640 or img_width != 640:
                if yolo_height - img_height > 0:
                    diff_height = yolo_height - img_height
                if yolo_width - img_width > 0:
                    diff_width = yolo_width - img_width

                self.frame = cv2.copyMakeBorder(self.frame, 0, diff_height, 0, diff_width, cv2.BORDER_CONSTANT, (0, 0, 0))
                # self.frame = cv2.copyMakeBorder(self.frame, 0, diff_height, 0, diff_width, cv2.BORDER_CONSTANT, (255, 255, 255))
                # img_height, img_width, channels = img.shape[:3]
                # print("img_pad_width: " + str(img_width))
                # print("img_pad_dst_height: " + str(img_height))

            # # 1:1でない画像のみ行う処理, 値が大きい方を基準にし、片方を黒でパディング
            # diff_height = 0
            # diff_width = 0
            # if img_height / img_width != 1:
            #     if img_height > img_width:
            #         diff_width = img_height - img_width
            #         self.frame = cv2.copyMakeBorder(self.frame, 0, diff_height, 0, diff_width, cv2.BORDER_CONSTANT, (0, 0, 0))
            #     else:
            #         diff_height = img_width - img_height
            #         self.frame = cv2.copyMakeBorder(self.frame, 0, diff_height, 0, diff_width, cv2.BORDER_CONSTANT, (0, 0, 0))

            # try:
            #     # self.frame = cv2.resize(self.frame, dsize=(416, 416))
            #     pass
            # except cv2.error as e:
            #     self.file_index += 1
            #     # self.read_data(i + 1)
            #     print("step: {}".format(i + 1))
            #     continue


            # 使用する画像の保存
            cv2.imwrite("/root/HSR/catkin_ws/src/create_prior/data/conv_img/{}.jpg".format(i + 1), self.frame)

            raw_img = self.cv_bridge.cv2_to_compressed_imgmsg(self.frame)
            self.object_server(i + 1, raw_img)

    def object_server(self, step, image):
        # if (os.path.exists("../data/tmp_boo/Object.csv") == True):
        #     with open("../data/tmp_boo/Object.csv", 'r') as f:
        #         reader = csv.reader(f)
        #         self.object_list = [row for row in reader]
            # print("pre_object_list: {}\n".format(self.object_list))


        timeout = time.time() + 3
        start = time.time()
        with tqdm() as pbar:
            while True:
                self.img_pub.publish(image)
                # print("Publish image: {}".format(str(time.time() - start)))
                if time.time() > timeout:
                    break

        self.file_index += 1

        timeout = time.time() + 3
        start = time.time()
        with tqdm() as pbar:
            while True:
                self.index_pub.publish(str(self.file_index))
                # print("Publish index: {}".format(str(time.time() - start)))
                if time.time() > timeout:
                    break

        self.read_data(step)

        return

    def extracting_label(self):
        object_list = []
        for i in range(len(self.detect_object_info[0])):
            object_list.append(self.detect_object_info[0][i])
            # print(object_list)
        self.object_list = object_list
        # print(self.object_list)
        return

    def make_object_boo(self):
        # print(self.object_list)
        self.Object_BOO = [0 for i in range(len(object_dictionary))]
        # print(self.Object_BOO)
        for j in range(len(self.object_list)):
            for i in range(len(object_dictionary)):
                if object_dictionary[i] == self.object_list[j]:
                    self.Object_BOO[i] = self.Object_BOO[i] + 1
        # print(self.Object_BOO)
        return

    def save_data(self, step):
        # # 全時刻の観測された物体のリストを保存
        # FilePath = "../data/tmp_boo/Object.csv"
        # with open(FilePath, 'w') as f:
        #     writer = csv.writer(f)
        #     writer.writerows(self.object_list)

        # 観測された物体のリストを保存
        FilePath = "../data/tmp_boo/" + str(step) + "_Object.csv"
        with open(FilePath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.object_list)

        # Bag-Of-Objects特徴量を保存
        FilePath = "../data/tmp_boo/" + str(step) + "_Object_BOO.csv"
        with open(FilePath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.Object_BOO)

        # 物体の辞書を保存
        FilePath = "../data/tmp_boo/" + str(step) + "_Object_W_list.csv"
        with open(FilePath, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(object_dictionary)

        return

    def read_data(self, step):
        if (os.path.exists(path + "/{}.jpg".format(self.file_index)) != True
             and os.path.exists(path + "/{}.csv".format(self.file_index)) != True):
            if step == 1:
                # 最初の教示で物体が検出されなかったとき
                self.object_list = []
                self.Object_BOO = [0] * len(object_dictionary)
                self.save_data(step)
                print("No object at the first step.")
                return

            else:
                # 最初の教示以降の教示で物体が検出されなかったとき
                object_list = []
                self.object_list = object_list
                self.make_object_boo()
                self.save_data(step)
                print("No object")
                return

        with open(path + "/{}.csv".format(self.file_index), 'r') as f:
            reader = csv.reader(f)
            self.detect_object_info = [row for row in reader]
        print("Save object")

        self.extracting_label()
        self.make_object_boo()
        self.save_data(step)
        return


    def scale_box(self, img, width, height):
        """指定した大きさに収まるように、アスペクト比を固定して、リサイズする。
        """
        h, w = img.shape[:2]
        aspect = w / h
        if width / height >= aspect:
            nh = height
            nw = round(nh * aspect)
        else:
            nw = width
            nh = round(nw / aspect)
        dst = cv2.resize(img, dsize=(nw, nh))
        return dst

if __name__ == '__main__':
    rospy.init_node('create_prior', anonymous=False)
    srv = ObjectFeatureServer()
    # rospy.spin()
