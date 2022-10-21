#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml

with open('./yolo9000.yaml', 'r') as yml:
    config_yolo9000 = yaml.load(yml)

yolo9000_object_dictionary = config_yolo9000['yolo_model']['detection_classes']['names']

with open('./Objects365.yaml', 'r') as yml:
    config = yaml.load(yml)

object_dictionary = config['names']

# print(object_dictionary[1054])
# print(len(object_dictionary))
