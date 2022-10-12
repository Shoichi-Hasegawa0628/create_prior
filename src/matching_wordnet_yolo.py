#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import wordnet_jp
import pprint
import sqlite3



with open('./yolo9000.yaml', 'r') as yml:
    config = yaml.load(yml)

object_dictionary = config['yolo_model']['detection_classes']['names']
print("YOLO9000のラベル数：{}".format(len(object_dictionary))) # yolo9000のラベル数は9418

# WordNetデータの内容の確認
# sqlite_masterという表から、nameという列のデータを取得
conn = sqlite3.connect("wnjpn.db")
cur = conn.execute("select count(*) from word")
for row in cur:
    print("Wordnetに登録されているWordDBの単語数：%s" % row[0]) #

count = 0
for w in range(len(object_dictionary)):
    synonym = wordnet_jp.getSynonym(object_dictionary[w])
    if len(synonym) == 0:
        # print(object_dictionary[w])
        count += 1

print("WordNetに登録されていないyoloのラベル数：{}".format(count)) # WordNetに登録されていないyoloのラベルは4005個

