from django.db import models
from django.contrib import admin
from user.models import UserExtension
from django.utils.timezone import now

# Create your models here.
# 轮播图
class Swiper(models.Model):

    del_choices = ( ('0', '未删除'),('1', '已删除'))
    
    now = str(now().strftime('%Y_%m'))

    name = models.CharField(max_length=60, verbose_name='content', help_text='content（CharField）')
    img = models.ImageField(upload_to='imgs/'+now, verbose_name='图片',help_text='图片（ImageField）', null=True, blank=True)
    path = models.TextField(verbose_name='跳转地址', help_text='跳转地址（TextField）', blank=True)

    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='swiper_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='swiper_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')

    class Meta:
        ordering = ['id']
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

@admin.register(Swiper)
class SwiperAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id', 'name', 'img', 'path','created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 提供引用查询
    search_fields=('name', )
    list_filter = ('created_date',)
    # 设置点击编辑字段
    list_display_links = ( 'id','name',)


    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)

class Notice(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    
    name = models.CharField(max_length=60, verbose_name='公告标题', help_text='公告标题（CharField）')
    text = models.TextField(verbose_name='公内内容', help_text='公内内容（TextField）', blank=True)
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='notice_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='notice_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')

    class Meta:
        ordering = ['-id']
        verbose_name = '公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

@admin.register(Notice)
class NoticeAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id', 'name', 'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 提供引用查询
    search_fields=('name', )
    list_filter = ('created_date',)
    # 设置点击编辑字段
    list_display_links = ( 'id','name',)


    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)