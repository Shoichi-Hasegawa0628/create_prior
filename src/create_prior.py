#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library
from __future__ import unicode_literals
import codecs
import cv2
from cv_bridge import CvBridge, CvBridgeError
import os
import csv

# Third Party
import numpy as np
import rospy
import actionlib
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
import darknet_ros_msgs.msg as darknet_ros_msgs
# import yolo_ros_msgs.msg as yolo_ros_msgs

# Self Modules
from __init__ import *

# from rgiro_spco2_slam.srv import spco_data_object, spco_data_objectResponse


class ObjectFeatureServer():
    def __init__(self):
        self.detect_object_info = []
        self.detect_image = 0
        self.object_list = []
        self.Object_BOO = []
        self.cv_bridge = CvBridge()
        self.frame = 0

        # self.client = actionlib.SimpleActionClient("/darknet_ros/check_for_objects", darknet_ros_msgs.CheckForObjectsAction)
        # self.client = actionlib.SimpleActionClient("/all_detection_data", yolo_ros_msgs.AllDetectionDataAction)
        self.client = actionlib.SimpleActionClient("/darknet_ros/all_detection_data",darknet_ros_msgs.AllDetectionDataAction)
        self.client.wait_for_server()

        rospy.loginfo("[Service spco_data/object] Ready")

        files = os.listdir("../data/image")
        for i in range(len(files)):
            self.frame = cv2.imread("../data/image/{}.jpg".format(i + 1))
            raw_img = self.cv_bridge.cv2_to_imgmsg(self.frame, encoding="bgr8")
            # raw_img = self.cv_bridge.cv2_to_compressed_imgmsg(self.frame)
            self.object_server(i + 1, raw_img)

    def object_server(self, step, image):
        if (os.path.exists("../data/tmp_boo/Object.csv") == True):
            with open("../data/tmp_boo/Object.csv", 'r') as f:
                reader = csv.reader(f)
                self.object_list = [row for row in reader]
            # print("pre_object_list: {}\n".format(self.object_list))

        # goal = darknet_ros_msgs.CheckForObjectsGoal(0, image)
        # goal = yolo_ros_msgs.AllDetectionDataGoal(0, image)
        goal = darknet_ros_msgs.AllDetectionDataGoal(0, image)
        self.client.send_goal_and_wait(goal)
        result = self.client.get_result()

        self.detect_object_info = result.bounding_boxes.bounding_boxes
        self.detect_image = result.detection_image
        # self.detect_image = result.detect_image
        # print(type(self.detect_image))

        if len(self.detect_object_info) == 0:
            if step == 1:
                # 最初の教示で物体が検出されなかったとき
                self.object_list = [[]]
                self.Object_BOO = [[0] * len(object_dictionary)]
                # self.taking_single_image(trialname, req.step)
                self.save_data(step)
                # return spco_data_objectResponse(True)
                print("O0")
                return

            else:
                # 最初の教示以降の教示で物体が検出されなかったとき
                object_list = []
                self.object_list.append(object_list)
                self.make_object_boo()
                # self.taking_single_image(trialname, req.step)
                self.save_data(step)
                # return spco_data_objectResponse(True)
                print("O000")
                return

        print(self.detect_image.header)
        self.save_detection_img(step, self.detect_image)
        self.extracting_label()
        self.make_object_boo()
        # self.taking_single_image(trialname, req.step)
        self.save_data(step)
        # print("object_list: {}\n".format(self.object_list))
        # print("dictionary: {}\n".format(object_dictionary))
        # print("Bag-of-Objects: {}\n".format(self.Object_BOO))
        # return spco_data_objectResponse(True)

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

    # def taking_single_image(self, trialname, step):
    #     img = rospy.wait_for_message('/hsrb/head_rgbd_sensor/rgb/image_rect_color/compressed', CompressedImage,
    #                                  timeout=None)
    #     observed_img = self.cv_bridge.compressed_imgmsg_to_cv2(img)
    #     cv2.imwrite(datafolder + trialname + "/object_image/" + str(step) + ".jpg", observed_img)
    #     return


    ######
    def save_detection_img(self, step, image):
        # img = rospy.wait_for_message('/yolov5_ros/output/image/compressed', CompressedImage, timeout=15)
        detect_img = self.cv_bridge.imgmsg_to_cv2(image, "bgr8")
        # detect_img = self.cv_bridge.compressed_imgmsg_to_cv2(image)
        cv2.imwrite("../data/detect_image/" + str(step) + ".png", detect_img)
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


if __name__ == '__main__':
    rospy.init_node('create_prior', anonymous=False)
    srv = ObjectFeatureServer()
    rospy.spin()
