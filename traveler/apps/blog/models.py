from django.db import models

# Create your models here.
# 帖子
# 帖子评论
from django.contrib import admin
from trip.models import Trip
from user.models import UserExtension
from mdeditor.fields import MDTextField
from django.utils.timezone import now
from files.models import Images

# Create your models here.
# 帖子属性
class BlogTags(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    name = models.CharField(max_length=60, verbose_name='帖子属性', help_text='帖子属性（CharField）')
    color = models.CharField(max_length=60, verbose_name='标签颜色', help_text='标签颜色（CharField）',default='#6190e8')
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='tags_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='tags_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        verbose_name = '帖子属性'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
@admin.register(BlogTags)
class BlogTagsAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id', 'name','color', 'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 提供引用查询
    search_fields=('name',)
    # 设置点击编辑字段
    list_display_links = ( 'id','name',)
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)


# 帖子
class Blog(models.Model):
    now = str(now().strftime('%Y_%m'))
    del_choices = ( ('0', '未删除'),('1', '已删除'))

    name = models.CharField(max_length=225, verbose_name='帖子名称', help_text='帖子名称（CharField）')
    img = models.ForeignKey(Images,  verbose_name='封面',help_text='封面（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='blog_img')
    trip = models.ForeignKey(Trip,  verbose_name='关联行程',help_text='关联行程（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='blog_trip')
    # image = models.ImageField(upload_to='imgs/Blog/'+now, verbose_name='封面',help_text='封面（ImageField）', null=True, blank=True)
    content = models.CharField(max_length=225, verbose_name='说明', help_text='说明（CharField）', blank=True)

    desc = MDTextField(verbose_name="帖子内容", blank=True)
    tags = models.ForeignKey(BlogTags,  verbose_name='帖子属性',help_text='帖子属性（ForeignKey）', null=True, blank=True, on_delete=models.SET_NULL, related_name='tags')
    show = models.BooleanField(verbose_name='是否公开可见',help_text='是否公开可见',default=True)
    editedDay = models.DateField(verbose_name='编辑日期', help_text='编辑日期（DateTimeField）', auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='blog_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='blog_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        ordering = ['-id']
        verbose_name = '帖子'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
@admin.register(Blog)
class BlogAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id', 'name','img','trip','content','desc','tags','show','editedDay','created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 提供引用查询
    search_fields=('name',)
    list_filter = ('name',)
    # 设置点击编辑字段
    list_display_links = ( 'id','name',)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)

# 帖子类型
class BlogType(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    name = models.CharField(max_length=60, verbose_name='帖子类型', help_text='帖子类型（CharField）')
    color = models.CharField(max_length=60, verbose_name='标签颜色', help_text='标签颜色（CharField）',default='#6190e8')
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='blogt_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='blogt_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        verbose_name = '帖子类型'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
@admin.register(BlogType)
class BlogTypeAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id', 'name','color', 'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 提供引用查询
    search_fields=('name',)
    # 设置点击编辑字段
    list_display_links = ( 'id','name',)
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)

# 帖子类型二联表
class Typ2Blog(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    blog = models.ForeignKey(Blog,  verbose_name='帖子',help_text='帖子（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    typ = models.ForeignKey(BlogType,  verbose_name='帖子类别',help_text='帖子类别（ForeignKey）', null=True, blank=True, on_delete=models.SET_NULL, related_name='typ')
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='typ2blog_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='typ2blog_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        ordering = ['-id']
        verbose_name = '帖子类型二联表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.blog.name) + '-' + str(self.typ.name)
@admin.register(Typ2Blog)
class Typ2BlogAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id', 'blog','typ','created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('blog','typ','created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 提供引用查询
    search_fields=('blog__name',)
    list_filter = ('typ__name',)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)

# 帖子评论
class BlogTalk(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    blog = models.ForeignKey(Blog,  verbose_name='帖子',help_text='帖子（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    desc = models.CharField(max_length=120, verbose_name='帖子评论', help_text='帖子评论（CharField）')
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='blogtalk_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='blogtalk_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        ordering = ['-id']
        verbose_name = '帖子评论'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.blog.name
@admin.register(BlogTalk)
class BlogTalkAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id','blog', 'desc', 'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('blog','created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 提供引用查询
    search_fields=('desc',)
    # 设置点击编辑字段
    list_display_links = ( 'id','desc',)
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)

class BlogPraise(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    blog = models.ForeignKey(Blog,  verbose_name='帖子',help_text='帖子（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='blogp_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='blogp_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        verbose_name = '帖子-用户-点赞'
        verbose_name_plural = verbose_name
        unique_together = ('blog', 'created_by',)
@admin.register(BlogPraise)
class BlogPraiseAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id','blog',  'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('blog', 'created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 设置点击编辑字段
    list_display_links = ( 'id',)
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)


class BlogCollect(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    blog = models.ForeignKey(Blog,  verbose_name='帖子',help_text='帖子（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='blogc_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='blogc_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        verbose_name = '帖子-用户-收藏'
        verbose_name_plural = verbose_name
        unique_together = ('blog', 'created_by',)
@admin.register(BlogCollect)
class BlogCollectAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id','blog',  'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('blog', 'created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 设置点击编辑字段
    list_display_links = ( 'id',)
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)