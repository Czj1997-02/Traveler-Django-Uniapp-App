#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
from .models import *
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.serializers import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 登录验证
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        return token

# 注册序列化
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

# 验证码
class TelCodeSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = TelCode
        fields = "__all__"
#first
class TelCodeOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = TelCode
        fields = ['value', ]
    
# 用户拓展信息
class UserExtensionSerializer(serializers.ModelSerializer):
    guanzhu = serializers.SerializerMethodField()
    fensi = serializers.SerializerMethodField()
    is_follow = serializers.SerializerMethodField()
    follow_id = serializers.SerializerMethodField()
    portrait_src = serializers.ImageField(source='portrait.portrait', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    cityname = serializers.CharField(source='city.name', read_only=True)
    # groups = serializers.SerializerMethodField()

    class Meta:
        model = UserExtension
        fields = "__all__"
    def get_guanzhu(self, obj):
        return Follow.objects.filter(deleted="0",created_by=obj).count()
    def get_fensi(self, obj):
        return Follow.objects.filter(deleted="0",follow=obj).count()
    def get_is_follow(self, obj):
        is_follow = Follow.objects.filter(deleted="0",created_by=self.context['request'].user.id,follow=obj).first()
        if is_follow:
            return True
        else:
            return False
    def get_follow_id(self, obj):
        is_follow = Follow.objects.filter(deleted="0",created_by=self.context['request'].user.id,follow=obj).first()
        if is_follow:
            return is_follow.id
        else:
            return False

# 用户拓展信息下拉选
class UserExtensionOptionSerializer(serializers.ModelSerializer):

    value = serializers.CharField(source='id', read_only=True)
    label = serializers.CharField(source='realname', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserExtension
        fields = ['value', 'label','username']
    
#first
class PortraitSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Portrait
        fields = "__all__"
    
#first
class PortraitOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = Portrait
        fields = ['value', ]
    
#addcity
class CitySerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = City
        fields = "__all__"
    
#addcity
class CityOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='name')

    class Meta:
        model = City
        fields = ['value', 'label']
    
# 城市树基本元素序列化器
class CityTreeChildSerializer(serializers.ModelSerializer):
    """
    城市树基本元素序列化器
    """
    class Meta:
        model = City
        fields = ['value', 'text']
# 城市树序列化器
class CityTreeParentSerializer(serializers.ModelSerializer):
    """
    城市树序列化器
    """
    children = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['value', 'text', 'children']

    def get_children(self, obj):
        depts = City.objects.filter(parent_id=obj.id)
        if depts:
            depts_list = CityTreeChildSerializer(depts, many=True, context={'request': self.context['request']}).data
        else:
            depts_list = []
        return depts_list
#增加用户关注表
class FollowSerializer(serializers.ModelSerializer):
    guanzhu = serializers.SerializerMethodField()
    fensi = serializers.SerializerMethodField()
    follow_portrait = serializers.ImageField(source='follow.portrait.portrait', read_only=True)
    follow_name = serializers.CharField(source='follow.realname', read_only=True)
    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Follow
        fields = "__all__"

    def get_guanzhu(self, obj):
        return Follow.objects.filter(deleted="0",created_by=obj.follow).count()
    def get_fensi(self, obj):
        return Follow.objects.filter(deleted="0",follow=obj.follow).count()
    
#增加用户关注表
class FollowOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='follow.realname', read_only=True)

    class Meta:
        model = Follow
        fields = ['value', 'label']
    