#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
from .models import *
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.serializers import *

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
class PlaceSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    images = serializers.SerializerMethodField()
    pagetyp = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    image2 = serializers.ImageField(source='img2.img', read_only=True)
    image3 = serializers.ImageField(source='img3.img', read_only=True)
    image4 = serializers.ImageField(source='img4.img', read_only=True)
    image5 = serializers.ImageField(source='img5.img', read_only=True)
    image6 = serializers.ImageField(source='img6.img', read_only=True)
    image7 = serializers.ImageField(source='img7.img', read_only=True)
    image8 = serializers.ImageField(source='img8.img', read_only=True)
    image9 = serializers.ImageField(source='img9.img', read_only=True)
    created_by_portrait = serializers.ImageField(source='created_by.portrait.portrait', read_only=True)
    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    # created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    # last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M')
    is_praise = serializers.SerializerMethodField() # 是否点赞
    is_collect = serializers.SerializerMethodField() # 是否收藏
    praise = serializers.SerializerMethodField()# 点赞数
    collect = serializers.SerializerMethodField()# 收藏数
    talk = serializers.SerializerMethodField()# 评论数
    select = serializers.SerializerMethodField()

    praise_id = serializers.SerializerMethodField()
    collect_id = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = "__all__"
    def get_praise_id(self, obj):
        Praise = PlacePraise.objects.filter(deleted='0',place=obj, created_by=self.context['request'].user.extension).first()
        if Praise:
            return Praise.id
    def get_collect_id(self, obj):
        Collect = PlaceCollect.objects.filter(deleted='0',place=obj, created_by=self.context['request'].user.extension).first()
        if Collect:
            return Collect.id
    def get_image(self, obj):
        if obj.img1:
            return self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img1.img)
        else:
            return self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/portrait/nopic.png'
    def get_images(self, obj):
        images = []
        if obj.img1:
            images.append(self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img1.img))
        if obj.img2:
            images.append(self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img2.img))
        if obj.img3:
            images.append(self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img3.img))
        if obj.img4:
            images.append(self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img4.img))
        if obj.img5:
            images.append(self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img5.img))
        if obj.img6:
            images.append(self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img6.img))
        if obj.img7:
            images.append(self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img7.img))
        if obj.img8:
            images.append(self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img8.img))
        if obj.img9:
            images.append(self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img9.img))
        return images
        # if obj.img1:
        #     images.append({'id':obj.img1.id,'content':obj.name + '[图1]','img':self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img1.img)})
        # if obj.img2:
        #     images.append({'id':obj.img2.id,'content':obj.name + '[图2]','img':self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img2.img)})
        # if obj.img3:
        #     images.append({'id':obj.img3.id,'content':obj.name + '[图3]','img':self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img3.img)})
        # if obj.img4:
        #     images.append({'id':obj.img4.id,'content':obj.name + '[图4]','img':self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img4.img)})
        # if obj.img5:
        #     images.append({'id':obj.img5.id,'content':obj.name + '[图5]','img':self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img5.img)})
        # if obj.img6:
        #     images.append({'id':obj.img6.id,'content':obj.name + '[图6]','img':self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img6.img)})
        # if obj.img7:
        #     images.append({'id':obj.img7.id,'content':obj.name + '[图7]','img':self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img7.img)})
        # if obj.img8:
        #     images.append({'id':obj.img8.id,'content':obj.name + '[图8]','img':self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img8.img)})
        # if obj.img9:
        #     images.append({'id':obj.img9.id,'content':obj.name + '[图9]','img':self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.img9.img)})
        # return images
    
    def get_select(self, obj):
        return False
    def get_praise(self, obj):
        return PlacePraise.objects.filter(deleted='0',place=obj).count()
    def get_collect(self, obj):
        return PlaceCollect.objects.filter(deleted='0',place=obj).count()
    def get_talk(self, obj):
        return PlaceTalk.objects.filter(deleted='0',place=obj).count()
    def get_is_praise(self, obj):
        is_praise = PlacePraise.objects.filter(deleted='0',place=obj, created_by=self.context['request'].user.extension)
        if is_praise:
            return True
        else:
            return False
    def get_is_collect(self, obj):
        is_collect = PlaceCollect.objects.filter(deleted='0',place=obj, created_by=self.context['request'].user.extension)
        if is_collect:
            return True
        else:
            return False
    def get_pagetyp(self, obj):
        return 'place'

#first
class PlaceOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = Place
        fields = ['value']
    
#first
class PlaceTypeSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = PlaceType
        fields = "__all__"
    
#first
class PlaceTypeOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = PlaceType
        fields = ['value']
    
#first
class Typ2PlaceSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Typ2Place
        fields = "__all__"
    
#first
class Typ2PlaceOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = Typ2Place
        fields = ['value']
    
#first
class PlaceTalkSerializer(serializers.ModelSerializer):
    portrait = serializers.ImageField(source='created_by.portrait.portrait', read_only=True)
    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = PlaceTalk
        fields = "__all__"
    
#first
class PlaceTalkOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = PlaceTalk
        fields = ['value']
    
#帖子行程地点点赞收藏
class PlacePraiseSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = PlacePraise
        fields = "__all__"
    
#帖子行程地点点赞收藏
class PlacePraiseOptionSerializer(serializers.ModelSerializer):

    # value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = PlacePraise
        # fields = ['value', 'label']
    
#帖子行程地点点赞收藏
class PlaceCollectSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = PlaceCollect
        fields = "__all__"
    
#帖子行程地点点赞收藏
class PlaceCollectOptionSerializer(serializers.ModelSerializer):

    # value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = PlaceCollect
        # fields = ['value', 'label']
    