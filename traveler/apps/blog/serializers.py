#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
from .models import *
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.serializers import *

# # 声明一个NewModel模型表单的序列化器
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
class BlogSerializer(serializers.ModelSerializer):
    trip_name = serializers.CharField(source='trip.name', read_only=True)
    trip_image = serializers.ImageField(source='trip.img.img', read_only=True)

    trip_created_by = serializers.CharField(source='trip.created_by.realname', read_only=True)
    # trip_created_date = serializers.DateTimeField(source='trip.created_date', read_only=True,required=False, format='%Y-%m-%d %H:%M:%S')
    trip_created_date = serializers.DateTimeField(source='trip.created_date', read_only=True,required=False, format='%Y-%m-%d %H:%M')

    pagetyp = serializers.SerializerMethodField()
    created_by_portrait = serializers.ImageField(source='created_by.portrait.portrait', read_only=True)
    image = serializers.ImageField(source='img.img', read_only=True)
    tags_name = serializers.CharField(source='tags.realname', read_only=True)
    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    # created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    # last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M')
    is_praise = serializers.SerializerMethodField() # 是否点赞
    is_collect = serializers.SerializerMethodField() # 是否收藏
    praise = serializers.SerializerMethodField() # 点赞数
    collect = serializers.SerializerMethodField()# 收藏数
    talk = serializers.SerializerMethodField()# 评论数
    select = serializers.SerializerMethodField()

    praise_id = serializers.SerializerMethodField()
    collect_id = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = "__all__"
    def get_praise_id(self, obj):
        Praise = BlogPraise.objects.filter(deleted='0',blog=obj, created_by=self.context['request'].user.extension).first()
        if Praise:
            return Praise.id
    def get_collect_id(self, obj):
        Collect = BlogCollect.objects.filter(deleted='0',blog=obj, created_by=self.context['request'].user.extension).first()
        if Collect:
            return Collect.id

    def get_select(self, obj):
        return False
    def get_praise(self, obj):
        return BlogPraise.objects.filter(deleted='0',blog=obj).count()
    def get_collect(self, obj):
        return BlogCollect.objects.filter(deleted='0',blog=obj).count()
    def get_talk(self, obj):
        return BlogTalk.objects.filter(deleted='0',blog=obj).count()
    def get_is_praise(self, obj):
        is_praise = BlogPraise.objects.filter(deleted='0',blog=obj, created_by=self.context['request'].user.extension)
        if is_praise:
            return True
        else:
            return False
    def get_is_collect(self, obj):
        is_collect = BlogCollect.objects.filter(deleted='0',blog=obj, created_by=self.context['request'].user.extension)
        if is_collect:
            return True
        else:
            return False
    
    def get_pagetyp(self, obj):
        return 'blog'

    
#first
class BlogOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = Blog
        fields = ['value']
    
#first
class BlogTypeSerializer(serializers.ModelSerializer):

    # created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    # created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    # last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    # last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = BlogType
        # fields = "__all__"
        fields = ['id','name','color']
    
#first
class BlogTypeOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = BlogType
        fields = ['value']
    
#first
class Typ2BlogSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Typ2Blog
        fields = "__all__"
    
#first
class Typ2BlogOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = Typ2Blog
        fields = ['value']
    
#first
class BlogTalkSerializer(serializers.ModelSerializer):
    portrait = serializers.ImageField(source='created_by.portrait.portrait', read_only=True)
    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = BlogTalk
        fields = "__all__"
    
#first
class BlogTalkOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = BlogTalk
        fields = ['value']
    
#tags
class BlogTagsSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = BlogTags
        fields = "__all__"
    
#tags
class BlogTagsOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id', read_only=True)
    text = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = BlogTags
        fields = ['value', 'text']
    
#帖子行程地点点赞收藏
class BlogPraiseSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = BlogPraise
        fields = "__all__"
    
#帖子行程地点点赞收藏
class BlogPraiseOptionSerializer(serializers.ModelSerializer):

    # value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = BlogPraise
        # fields = ['value', 'label']
    
#帖子行程地点点赞收藏
class BlogCollectSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = BlogCollect
        fields = "__all__"
    
#帖子行程地点点赞收藏
class BlogCollectOptionSerializer(serializers.ModelSerializer):

    # value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = BlogCollect
        # fields = ['value', 'label']
    