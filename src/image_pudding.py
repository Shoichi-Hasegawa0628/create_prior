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


img = cv2.imread(path + "pre_img/large_img.jpg")
# img = cv2.imread(path + "pre_img/small_img.jpg")

img_height, img_width, channels = img.shape[:3]
# print("width: " + str(img_width))
# print("height: " + str(img_height))

# 画像サイズのパターン → 4パターン、問題なのは大きいとき
## どちらか片方でも大 → 具体的にどちらが大きいかを明示 → オリジナル画像のアスペクト比を維持した状態でギリギリまで縮小 (範囲内かを確認) → 黒色でパディング
## paddingh  to fit propositon of yolo input

if img_width > yolo_width or img_height > yolo_height:
    dst = scale_box(img, 640, 640)
    print(f"{img.shape} -> {dst.shape}")
    img = dst
    img_height, img_width, channels = img.shape[:3]
    print("dst_width: " + str(img_width))
    print("dst_height: " + str(img_height))
    # cv2.imshow('color', dst)  # この時点ではウィンドウは表示されない
    # cv2.waitKey(0)  # ここで初めてウィンドウが表示される

diff_height = 0
diff_width = 0
# 640×640に合わせる処理
# if img_height != 640 or img_width != 640:
#     if yolo_height - img_height > 0:
#         diff_height = yolo_height - img_height
#     if yolo_width - img_width > 0:
#         diff_width = yolo_width - img_width
#
#     img = cv2.copyMakeBorder(img, 0, diff_height, 0, diff_width, cv2.BORDER_CONSTANT, (0,0,0))
#     img_height, img_width, channels = img.shape[:3]
#     print("img_pad_width: " + str(img_width))
#     print("img_pad_dst_height: " + str(img_height))

# 1:1でない画像のみ行う処理, 値が大きい方を基準にし、片方を黒でパディング
if img_height / img_width != 1:
    if img_height > img_width:
        diff_width = img_height - img_width
        img = cv2.copyMakeBorder(img, 0, diff_height, 0, diff_width, cv2.BORDER_CONSTANT, (0, 0, 0))
    else:
        diff_height = img_width - img_height
        img = cv2.copyMakeBorder(img, 0, diff_height, 0, diff_width, cv2.BORDER_CONSTANT, (0, 0, 0))


# cv2.imshow('color', img)  # この時点ではウィンドウは表示されない
# cv2.waitKey(0)  # ここで初めてウィンドウが表示される



