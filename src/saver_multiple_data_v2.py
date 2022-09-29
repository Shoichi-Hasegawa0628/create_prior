#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ROSで複数のメッセージを同時に受け取るプログラム

# Standardライブラリ
import os
import cv2
from cv_bridge import CvBridge, CvBridgeError

# ROSのライブラリ
import rospy
import message_filters
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String

path = "/root/HSR/catkin_ws/src/create_prior/data/output"


class SaverMultipleData():
    def __init__(self):
        self.cv_bridge = CvBridge()
        self.index_sub = rospy.Subscriber("/file_index", String, self.index_callback)
        self.sub1 = message_filters.Subscriber('/yolov5_ros/output/bounding_boxes', BoundingBoxes)
        self.sub2 = message_filters.Subscriber('/yolov5_ros/output/image/compressed', CompressedImage)

        delay = 0
        ts = message_filters.ApproximateTimeSynchronizer([self.sub1, self.sub2], 10, delay)
        ts.registerCallback(self.callback)
        self.file_index = 0

    def callback(self, msg1, msg2):
        detect_object_info = msg1
        img = msg2

        # 観測ラベルの確保
        object_list = []
        for i in range(len(detect_object_info)):
            object_list.append(detect_object_info[i].Class)
            print(object_list)
        object_list.append(object_list)

        # 検出画像の確保
        detect_img = self.cv_bridge.compressed_imgmsg_to_cv2(img)
        self.save_data(detect_img, object_list)
        return

    def save_data(self, img, list):
        # すでにファイルが存在していた場合は処理をスキップする
        if (os.path.exists(path + "/{}.jpg".format(self.file_index)) == True
                and os.path.exists(path + "/{}.csv".format(self.file_index)) == True):
            return

        # 検出画像の保存
        cv2.imwrite(path + "/{}.jpg".format(self.file_index), img)

        # 物体リストの保存
        FilePath = path + "/{}.csv".format(self.file_index)
        with open(FilePath, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(object_list)

        return

    def index_callback(self, msg):
        self.file_index = msg.data
        return


if __name__ == '__main__':
    rospy.init_node('saver_multiple_data')
    saver_multiple_data = SaverMultipleData()
    rospy.spin()
