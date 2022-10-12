#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
from cv_bridge import CvBridge, CvBridgeError

path = "/root/HSR/catkin_ws/src/create_prior/data/"
yolo_width = 640
yolo_height = 640

def scale_box(img, width, height):
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


large_img = cv2.imread(path + "pre_img/large_img.jpg")
small_img = cv2.imread(path + "pre_img/small_img.jpg")

img_height, img_width, channels = large_img.shape[:3]
print("width: " + str(img_width))
print("height: " + str(img_height))

# 画像サイズのパターン → 4パターン、問題なのは大きいとき
## どちらか片方でも大 → 具体的にどちらが大きいかを明示 → オリジナル画像のアスペクト比を維持した状態でギリギリまで縮小 (範囲内かを確認) → 黒色でパディング
## ひとまず、padding not

if img_width > yolo_width or img_height > yolo_height:
    dst = scale_box(large_img, 640, 640)
    print(f"{large_img.shape} -> {dst.shape}")
    # cv2.imshow('color', dst)  # この時点ではウィンドウは表示されない
    # cv2.waitKey(0)  # ここで初めてウィンドウが表示される

else:






