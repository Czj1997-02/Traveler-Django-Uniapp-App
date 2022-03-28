#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
一个快速自写基础序列化代码及视图代码的脚本：
"""

import os,re
import sys
import shutil

import os
paths = ['apps/' + name  for name in os.listdir('apps') ]

def write_serializers(path,name):
    # 读取原有内容
    f = open(path+ '/serializers.py',"r",encoding="utf-8")
    this_serializers = f.read()
    f.close()

    addcode = '\n#'+ str(sys.argv[1]) + '\nclass ' + name + """Serializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source='created_by.realname', read_only=True)
    created_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    last_edited_by_name = serializers.CharField(source='last_edited_by.realname', read_only=True)
    last_edited_date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = """ + name + """
        fields = "__all__"
    """

    # 把新内容写入文件
    if 'class ' + name + 'Serializer(serializers.ModelSerializer):' not in this_serializers:
        f = open(path + "/serializers.py","w",encoding="utf-8")
        f.write(this_serializers + addcode)
        f.close()

def write_Optionserializers(path,name):
    # 读取原有内容
    f = open(path+ '/serializers.py',"r",encoding="utf-8")
    this_serializers = f.read()
    f.close()

    addcode = '\n#'+ str(sys.argv[1]) + '\nclass ' + name + """OptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='name')

    class Meta:
        model = """ + name + """
        fields = ['value', 'label']
    """

    # 把新内容写入文件
    if 'class ' + name + 'OptionSerializer(serializers.ModelSerializer):' not in this_serializers:
        f = open(path + "/serializers.py","w",encoding="utf-8")
        f.write(this_serializers + addcode)
        f.close()


def write_views(path,name):
    # 读取原有内容
    f = open(path+ '/views.py',"r",encoding="utf-8")
    this_views = f.read()
    f.close()

    addcode = '\n#'+ str(sys.argv[1]) + '\nclass ' + name + """Views(MyModelViewSet):

    queryset = """ + name + """.objects.filter(deleted__exact='0')
    serializer_class = """ + name + """Serializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id','name']
    #search_fields = ['realname', 'user__username']
    """

    # 把新内容写入文件
    if 'class ' + name + 'Views(MyModelViewSet):' not in this_views:
        f = open(path + "/views.py","w",encoding="utf-8")
        f.write(this_views + addcode)
        f.close()

def write_Optionviews(path,name):
    # 读取原有内容
    f = open(path+ '/views.py',"r",encoding="utf-8")
    this_views = f.read()
    f.close()

    addcode = '\n#'+ str(sys.argv[1]) + '\nclass ' + name + """OptionViews(MyModelViewSet):

    queryset = """ + name + """.objects.filter(deleted__exact='0')
    serializer_class = """ + name + """OptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id','name']
    search_fields = ['name',]
    """

    # 把新内容写入文件
    if 'class ' + name + 'OptionViews(MyModelViewSet):' not in this_views:
        f = open(path + "/views.py","w",encoding="utf-8")
        f.write(this_views + addcode)
        f.close()

for path in paths:
    f = open(path+ '/models.py',"r",encoding="utf-8")
    this_data = f.readlines()
    for this_data_line in this_data:
        if 'class' in this_data_line and '(models.Model):' in this_data_line and '#' not in this_data_line:
            # print(re.split(r' |\(',this_data_line)[1])
            write_serializers(path,str(re.split(r' |\(',this_data_line)[1]))
            write_Optionserializers(path,str(re.split(r' |\(',this_data_line)[1]))
            write_views(path,str(re.split(r' |\(',this_data_line)[1]))
            write_Optionviews(path,str(re.split(r' |\(',this_data_line)[1]))