#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml

with open('./yolo9000.yaml', 'r') as yml:
    config = yaml.load(yml)

object_dictionary = config['yolo_model']['detection_classes']['names']
print(object_dictionary[1054])
print(len(object_dictionary))