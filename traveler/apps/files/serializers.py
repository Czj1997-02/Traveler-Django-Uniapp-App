#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
from .models import *
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.serializers import *
from PIL import Image

# 声明一个NewModel模型表单的序列化器
# class NewModelSerializer(serializers.ModelSerializer):

#     # 序列化处理方法，用来获取对应字段对应外键的其他内容，比如用户id的用户名
#     new_Char = serializers.CharField(source='某字段.对应外键', read_only=True)

#     # 序列化处理方法，用来处理让时间按特定格式显示
#     date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

#     # 序列化处理方法，用来处理显示模型中没有的字段
#     new_serializer_name = serializers.SerializerMethodField()

#     class Meta:
#         model = NewModel
#         fields = "__all__"

#     # 编写想要自定义的序列化处理方法
#     def get_new_serializer_name(self, obj):
#         # 在这里写处理逻辑，并修改返回内容
#         return obj.id



#first
class ImagesSerializer(serializers.ModelSerializer):



    url = serializers.ImageField(source='img', read_only=True)
    img_url = serializers.ImageField(source='img', read_only=True)
    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Images
        fields = "__all__"
    # def create(self, validated_data):
    #     '''序列化器重写创建实例'''
    #     newImages = Images()
    #     # 传入参数
    #     if 'with_models' in validated_data:
    #         newImages.with_models = validated_data["with_models"]
    #     if 'models_id' in validated_data:
    #         newImages.models_id = validated_data["models_id"]
    #     newImages.created_by = self.context['request'].user.extension
    #     newImages.last_edited_by = self.context['request'].user.extension
    #     picture = validated_data["img"]
    #     newImages.img = picture
    #     newImages.save()
    #     img = Image.open(os.path.dirname(__file__) +
    #                      '/../../media/' + str(newImages.img))
    #     if 'height' in validated_data:
    #         # print(validated_data['height'])
    #         x = img.height / int(validated_data['height'])
    #         w = int(img.width / x)
    #         new_img = img.resize((w, int(validated_data['height'])), Image.ANTIALIAS)
    #         new_img.save(os.path.dirname(__file__) +
    #                     '/../../media/' + str(newImages.img), quality = 95)
        
    #     # if img.height >= 240:
    #     #     x = img.height / 240
    #     #     w = int(img.width / x)
    #     #     new_img = img.resize((w, 240), Image.ANTIALIAS)
    #     #     new_img.save(os.path.dirname(__file__) +
    #     #                 '/../../media/' + str(newImages.img), quality = 95)
    #     else:
    #         pass
    #     return newImages
    
#first
class ImagesOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = Images
        fields = ['value']
    
#first
class FilesSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Files
        fields = "__all__"
    
#first
class FilesOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = Files
        fields = ['value',]
    