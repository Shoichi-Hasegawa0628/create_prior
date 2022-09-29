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
import actionlib
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
# import darknet_ros_msgs.msg as darknet_ros_msgs
import yolo_ros_msgs.msg as yolo_ros_msgs

# Self Modules
from __init__ import *

# 画像を読み込み → 指定した時間で画像を配信 → yoloの検出結果を別のノードが受け取り、結果をcreate_priorに渡す → BoO作成 → 保存 → 画像枚数だけ繰り返す


class ObjectFeatureServer():
    def __init__(self):
        self.detect_object_info = []
        self.detect_image = 0
        self.object_list = []
        self.Object_BOO = []
        self.cv_bridge = CvBridge()
        self.frame = 0
        self.sub = rospy.Subscriber("/yolov5_ros/output/bounding_boxes", yolo_ros_msgs.BoundingBoxes, self.callback)

    def callback(self, msg):
        print(type(msg))
        # 欲しいのはラベル




if __name__ == '__main__':
    rospy.init_node('create_prior', anonymous=False)
    srv = ObjectFeatureServer()
    rospy.spin()
