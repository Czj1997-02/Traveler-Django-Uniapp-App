#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
一个创建应用模块的脚本：
创建应用时同步创建序列化文件serializers.py
并移动文件夹到对应路径app
"""

import os
import sys
import shutil
import manage

"""
获取参数：应用模块名
"""

os.system('python manage.py startapp ' + str(sys.argv[1]))

"""
一些基础的序列化器导入
"""

some_import = """#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
from .models import *
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.serializers import *

# 声明一个NewModel模型表单的序列化器
class NewModelSerializer(serializers.ModelSerializer):

    # 序列化处理方法，用来获取对应字段对应外键的其他内容，比如用户id的用户名
    new_Char = serializers.CharField(source='某字段.对应外键', read_only=True)

    # 序列化处理方法，用来处理让时间按特定格式显示
    date = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    # 序列化处理方法，用来处理显示模型中没有的字段
    new_serializer_name = serializers.SerializerMethodField()

    class Meta:
        model = NewModel
        fields = "__all__"

    # 编写想要自定义的序列化处理方法
    def get_new_serializer_name(self, obj):
        # 在这里写处理逻辑，并修改返回内容
        return obj.id


"""

"""
在路径写好基础serializers.py文件
"""
f = open(str(sys.argv[1]) + "\serializers.py","w",encoding="utf-8")
f.write(some_import)
f.close()

some_import2 = """#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import django_filters
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.timezone import now, localtime
from .models import *

# 过滤器
class XXXFilter(django_filters.rest_framework.FilterSet):
    XXX = django_filters.CharFilter(help_text='XXX', method='filter_XXX')

    def filter_XXX(self, queryset, name, value):
        model = self.request.query_params['model']
        return queryset.filter(deleted__exact='0').filter()

    class Meta:
        model = XXX
        fields = ['XXX',]
"""

"""
在路径写好基础filters.py文件
"""
f = open(str(sys.argv[1]) + "/filters.py","w",encoding="utf-8")
f.write(some_import2)
f.close()

shutil.move(str(sys.argv[1]),"apps/" + str(sys.argv[1]))