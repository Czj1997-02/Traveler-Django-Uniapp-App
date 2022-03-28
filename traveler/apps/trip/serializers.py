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
class TripSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='img.img', read_only=True)
    pagetyp = serializers.SerializerMethodField()
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
    places = serializers.SerializerMethodField()# 对应行程点
    select = serializers.SerializerMethodField()

    praise_id = serializers.SerializerMethodField()
    collect_id = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = "__all__"

    def get_praise_id(self, obj):
        Praise = TripPraise.objects.filter(deleted='0',trip=obj, created_by=self.context['request'].user.extension).first()
        if Praise:
            return Praise.id
    def get_collect_id(self, obj):
        Collect = TripCollect.objects.filter(deleted='0',trip=obj, created_by=self.context['request'].user.extension).first()
        if Collect:
            return Collect.id

    def get_select(self, obj):
        return False
    def get_praise(self, obj):
        return TripPraise.objects.filter(deleted='0',trip=obj).count()
    def get_collect(self, obj):
        return TripCollect.objects.filter(deleted='0',trip=obj).count()
    def get_talk(self, obj):
        return TripTalk.objects.filter(deleted='0',trip=obj).count()
    def get_is_praise(self, obj):
        is_praise = TripPraise.objects.filter(deleted='0',trip=obj, created_by=self.context['request'].user.extension)
        if is_praise:
            return True
        else:
            return False
    def get_is_collect(self, obj):
        is_collect = TripCollect.objects.filter(deleted='0',trip=obj, created_by=self.context['request'].user.extension)
        if is_collect:
            return True
        else:
            return False
    def get_pagetyp(self, obj):
        return 'trip'
    def get_places(self, obj):
        places = PlacesInTrip.objects.filter(deleted='0',trip=obj).order_by('index')
        place_list = PlacesInTripSerializer(places,many=True).data
        for place in place_list:
            if 'icon' in place:
                place['icon'] = self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + place['icon']
                place['place_image'] = self.context['request'].META['wsgi.url_scheme'] + '://' + self.context['request'].META['HTTP_HOST'] + place['place_image']
        return place_list
#first
class TripOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = Trip
        fields = ['value']
    
#first
class TripTypeSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = TripType
        fields = "__all__"
    
#first
class TripTypeOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = TripType
        fields = ['value']
    
#first
class Typ2TripSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Typ2Trip
        fields = "__all__"
    
#first
class Typ2TripOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = Typ2Trip
        fields = ['value']
    
#first
class TripTalkSerializer(serializers.ModelSerializer):
    portrait = serializers.ImageField(source='created_by.portrait.portrait', read_only=True)
    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = TripTalk
        fields = "__all__"
    
#first
class TripTalkOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = TripTalk
        fields = ['value']
    
#帖子行程地点点赞收藏
class TripPraiseSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = TripPraise
        fields = "__all__"
    
#帖子行程地点点赞收藏
class TripPraiseOptionSerializer(serializers.ModelSerializer):

    # value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = TripPraise
        # fields = ['value', 'label']
    
#帖子行程地点点赞收藏
class TripCollectSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = TripCollect
        fields = "__all__"
    
#帖子行程地点点赞收藏
class TripCollectOptionSerializer(serializers.ModelSerializer):

    # value = serializers.IntegerField(source='id')
    # label = serializers.CharField(source='name')

    class Meta:
        model = TripCollect
        # fields = ['value', 'label']
    
#增加行程地点明细
class PlacesInTripSerializer(serializers.ModelSerializer):

    trip_name = serializers.CharField(source='trip.name', read_only=True)
    place_name = serializers.CharField(source='place.name', read_only=True)
    the_date = serializers.DateField(source='theDate', read_only=True)
    the_begin = serializers.TimeField(source='theBegin', read_only=True)
    icon = serializers.ImageField(source='place.img1.img', read_only=True)

    lat = serializers.DecimalField(source='place.lat', read_only=True,max_digits=30, decimal_places=20)
    lng = serializers.DecimalField(source='place.lng', read_only=True,max_digits=30, decimal_places=20)
    place_image = serializers.ImageField(source='place.img1.img', read_only=True) #img
    place_created_by_name = serializers.CharField(source='place.created_by.realname', read_only=True)
    place_typ = serializers.CharField(source='place.typ', read_only=True)
    place_created_date = serializers.DateTimeField(source='place.created_date', required=False, format='%Y-%m-%d %H:%M:%S', read_only=True)
    place_pagetyp  = serializers.SerializerMethodField()
    # icon = serializers.SerializerMethodField()

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = PlacesInTrip
        fields = "__all__"

    # def get_icon(self, obj):
    #     return self.context['request'].META['HTTP_HOST'] + '/media/' + str(obj.place.img1.img)
    def get_place_pagetyp(self, obj):
        return 'place'
#增加行程地点明细
class PlacesInTripOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='name')

    class Meta:
        model = PlacesInTrip
        fields = ['value', 'label']
    