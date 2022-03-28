from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password, check_password
# from rest_framework.authtoken.admin import TokenAdmin


admin.site.site_header = "Traveler"
admin.site.site_title = '后台管理'
