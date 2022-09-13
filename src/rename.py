#! /usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os

# 拡張子.txtのファイルを取得する
path = '../data/material/livingroom/*.jpg'
i = 0

# txtファイルを取得する
flist = glob.glob(path)
print('変更前')
print(flist)

# ファイル名を一括で変更する
for file in flist:
    os.rename(file, '../data/rename/' + str(i+1) + '.jpg')
    i += 1

list = glob.glob(path)
print('変更後')
print(list)




