#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ROSで複数のメッセージを同時に受け取るプログラム

import rospy
import message_filters
from sensor_msgs.msg import CompressedImage

import cv2
from cv_bridge import CvBridge, CvBridgeError

path = "/root/HSR/catkin_ws/src/saver_multiple_data/data"

class SaverMultipleData():
    def __init__(self):
        self.cv_bridge = CvBridge()


    def callback(self, msg1, msg2):
        img1 = msg1
        img2 = msg2
        out = [img1, img2]
        print(out)

        rgb_img = self.cv_bridge.compressed_imgmsg_to_cv2(img1)
        detect_img = self.cv_bridge.compressed_imgmsg_to_cv2(img2)
        cv2.imwrite(path + "/rgb_img.jpg", rgb_img)
        cv2.imwrite(path + "/detect_img.jpg", detect_img)
        print("Save !")


if __name__ == '__main__':
    rospy.init_node('saver_multiple_data')
    saver_multiple_data = SaverMultipleData()
    sub1 = message_filters.Subscriber('/hsrb/head_rgbd_sensor/rgb/image_rect_color/compressed', CompressedImage)
    sub2 = message_filters.Subscriber('/yolov5_ros/output/image/compressed', CompressedImage)

    delay = 0.005
    ts = message_filters.ApproximateTimeSynchronizer([sub1, sub2], 10, delay)
    ts.registerCallback(saver_multiple_data.callback)
    rospy.spin()


