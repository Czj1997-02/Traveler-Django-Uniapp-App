from django.conf import settings
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib.admin.options import get_ul_class
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.timezone import now

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework.authtoken.models import Token
from tool.txt2pic import txt2pic

# 创建token
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

# 验证码对应
class TelCode(models.Model):
    telephone = models.CharField(max_length=20, verbose_name='电话', help_text='电话（CharField）',blank=True)
    code =  models.CharField(max_length=10, verbose_name='验证码', help_text='验证码（CharField）', blank=True)
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True,auto_now_add=True)
    class Meta:
        verbose_name = '验证码对应'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.telephone
@admin.register(TelCode)
class TelCodeAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id','telephone', 'code','created_date')

# 用户拓展信息
class UserExtension(models.Model):
    sex_choices = ( ('0', '男'), ('1', '女') )
    user = models.OneToOneField(User, verbose_name='用户ID', help_text='用户ID（OneToOneField）', on_delete=models.CASCADE, related_name='extension')
    portrait = models.ForeignKey('Portrait', verbose_name='用户头像', null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey('City', verbose_name='城市', null=True, blank=True, on_delete=models.SET_NULL)
    realname = models.CharField(max_length=30, verbose_name='真实姓名', help_text='真实姓名（CharField）', blank=True)
    desc = models.CharField(max_length=120, verbose_name='个性签名', help_text='个性签名（CharField）', blank=True)
    project = models.TextField(verbose_name='可见项目', help_text='可见模块（TextField）', blank=True)
    modules = models.TextField(verbose_name='可见模块', help_text='可见模块（TextField）', blank=True)
    sex = models.CharField(max_length=1, verbose_name='性别', help_text='性别（CharField，可选值：0，1）', blank=True, choices=sex_choices, default='0')
    telephone = models.CharField(max_length=20, verbose_name='电话', help_text='电话（CharField）',blank=True, unique=True)
    birthday = models.DateField(verbose_name='生日', help_text='生日（DateField）', null=True, blank=True)
    visits = models.PositiveIntegerField(verbose_name='访问次数', help_text='访问次数（PositiveIntegerField）', null=True, blank=True,default=0)
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.realname
@admin.register(UserExtension)
class UserExtensionAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id','user','portrait','city', 'realname','desc', 'project','modules', 'sex', 'telephone', 'birthday')
    # 使用到外键下拉的字段
    autocomplete_fields = ('user',)
    # 开放操作动作
    actions_on_bottom = True
    # 提供引用查询
    search_fields = ('user__username', 'realname',)
    # 设置点击编辑字段
    list_display_links = ( 'id','realname','user')
    # def change_modules(self, request, queryset):
    #     queryset.update(modules = ',1,2,3,4,5,6,7,8,9,10,11,')
    # change_modules.short_description = "重置用户可见菜单"
    # actions = (change_modules,)

# 用户关注表
class Follow(models.Model):
    del_choices = ( ('0', '未删除'), ('1', '已删除'))
    follow = models.ForeignKey(UserExtension, verbose_name='关注', help_text='关注（ForeignKey）', null=True, blank=True,on_delete=models.SET_NULL, related_name='follow')
    created_by = models.ForeignKey(UserExtension, verbose_name='创建人ID', help_text='创建人ID（ForeignKey）', null=True, blank=True,on_delete=models.SET_NULL, related_name='follow_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True,auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension, verbose_name='最后编辑人ID', help_text='最后编辑人ID（ForeignKey）', null=True,blank=True, on_delete=models.SET_NULL, related_name='follow_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True,blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）',choices=del_choices, default='0')
    class Meta:
        verbose_name = '用户关注'
        verbose_name_plural = verbose_name
        unique_together = ('follow', 'created_by',)
        def __str__(self):
            return self.follow
@admin.register(Follow)
class FollowAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id','follow',  'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('follow', 'created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 设置点击编辑字段
    list_display_links = ( 'id',)
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)
# 肖像图片
class Portrait(models.Model):
    """
    肖像图片
    """
    del_choices = ( ('0', '未删除'), ('1', '已删除'))
    portrait = models.ImageField(upload_to='img/user/portrait', verbose_name='头像', help_text='头像（ImageField）',blank=True)
    created_by = models.ForeignKey(UserExtension, verbose_name='创建人ID', help_text='创建人ID（ForeignKey）', null=True, blank=True,on_delete=models.SET_NULL, related_name='portrait_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True,auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension, verbose_name='最后编辑人ID', help_text='最后编辑人ID（ForeignKey）', null=True,blank=True, on_delete=models.SET_NULL, related_name='portrait_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True,blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）',choices=del_choices, default='0')
    class Meta:
        ordering = ['-id']
        verbose_name = '肖像图片'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.portrait)

@admin.register(Portrait)
class PortraitAdminModel(admin.ModelAdmin):
    list_per_page = 50
    actions_on_bottom = True
    list_display = ('id', 'portrait', 'created_by', 'created_date', 'last_edited_by', 'last_edited_date', 'deleted')
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)

# 城市
class City(models.Model):
    """城市"""
    del_choices = ( ('0', '未删除'), ('1', '已删除'))
    name = models.CharField(max_length=225, verbose_name='名称', help_text='名称（CharField）')
    level = models.PositiveIntegerField(verbose_name='层级', help_text='层级（PositiveIntegerField）', null=True, blank=True)
    parent = models.ForeignKey('self', verbose_name='父级', null=True, blank=True, on_delete=models.PROTECT, related_name='child')
    # country = models.CharField(max_length=225, verbose_name='所属国家', help_text='所属国家（CharField）', blank=True)
    # province = models.CharField(max_length=225, verbose_name='所属省份', help_text='所属省份（CharField）', blank=True)
    wens = models.CharField(max_length=225, verbose_name='经纬度', help_text='经纬度（CharField）', blank=True)
    created_by = models.ForeignKey(UserExtension, verbose_name='创建人ID', help_text='创建人ID（ForeignKey）', null=True, blank=True,on_delete=models.SET_NULL, related_name='city_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True,auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension, verbose_name='最后编辑人ID', help_text='最后编辑人ID（ForeignKey）', null=True,blank=True, on_delete=models.SET_NULL, related_name='city_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True,blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）',choices=del_choices, default='0')
    class Meta:
        ordering = ['-id']
        verbose_name = '城市'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
@admin.register(City)
class CityAdminModel(admin.ModelAdmin):
    list_per_page = 50
    actions_on_bottom = True
    # list_display = ('id', 'name','country','province','wens', 'created_by', 'created_date', 'last_edited_by', 'last_edited_date', 'deleted')
    list_display = ('id', 'name','level','parent','wens', 'created_by', 'created_date', 'last_edited_by', 'last_edited_date', 'deleted')
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)
    
# 同步创建用户拓展信息功能
@receiver(post_save, sender=User)
def create_user_extension(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user = instance)
    else:
        instance.extension.save()
        
# @receiver(post_save, sender=User)
# def create_user_extension(sender, instance, created, **kwargs):
#     if created:
#         userobj = UserExtension.objects.create(user=instance)
#         if instance.last_name + instance.first_name == '':
#             okpath = txt2pic(str(instance.username),r'media/img/portraits')
#             okpath = okpath.replace('media/','')
#             userobj.portrait = create_auto_portrait(okpath, instance.username)
#             userobj.save()

#         else:
#             okpath = txt2pic(str(instance.last_name + instance.first_name),r'media/img/portraits')
#             okpath = okpath.replace('media/','')
#             userobj.portrait = create_auto_portrait(okpath, instance.username)
#             userobj.save()

#     else:
#         if instance.extension.portrait:
#             instance.extension.save()
#         else:
#             userobj = instance.extension
#             if instance.last_name + instance.first_name == '':
#                 okpath = txt2pic(str(instance.username),r'media/img/portraits')
#                 okpath = okpath.replace('media/','')
#                 userobj.portrait = create_auto_portrait(okpath, instance.extension)
#                 userobj.save()

#             else:
#                 okpath = txt2pic(str(instance.last_name + instance.first_name),r'media/img/portraits')
#                 okpath = okpath.replace('media/','')
#                 userobj.portrait = create_auto_portrait(okpath, instance.extension)
#                 userobj.save()


# def create_auto_portrait(img_path, created_by):
#     portrait = Portrait()
#     portrait.portrait = img_path
#     portrait.created_by = created_by
#     portrait.save()
#     return portrait