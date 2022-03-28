from django.db import models

# Create your models here.
# 行程
# 行程评论
from django.contrib import admin
from user.models import UserExtension
from mdeditor.fields import MDTextField
from place.models import Place

# Create your models here.
# 行程
from files.models import Images

class Trip(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    name = models.CharField(max_length=225, verbose_name='行程名称', help_text='行程名称（CharField）')
    desc = MDTextField(verbose_name="行程内容", blank=True)
    img = models.ForeignKey(Images,  verbose_name='封面',help_text='封面（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='Trip_img')

    show = models.BooleanField(verbose_name='是否公开可见',help_text='是否公开可见',default=True)
    editedDay = models.DateField(verbose_name='编辑日期', help_text='编辑日期（DateTimeField）', auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='trip_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='trip_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        ordering = ['-id']
        verbose_name = '行程'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
@admin.register(Trip)
class TripAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id', 'name','desc','img','show','editedDay','created_by', 'created_date', 'last_edited_by','last_edited_date')
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

# 行程类型
class TripType(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    name = models.CharField(max_length=60, verbose_name='行程类型', help_text='行程类型（CharField）')
    color = models.CharField(max_length=60, verbose_name='标签颜色', help_text='标签颜色（CharField）',default='#6190e8')
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='tript_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='tript_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        verbose_name = '行程类型'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
@admin.register(TripType)
class TripTypeAdminModel(admin.ModelAdmin):
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

# 行程类型二联表
class Typ2Trip(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    trip = models.ForeignKey(Trip,  verbose_name='行程',help_text='行程（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    typ = models.ForeignKey(TripType,  verbose_name='行程类别',help_text='行程类别（ForeignKey）', null=True, blank=True, on_delete=models.SET_NULL, related_name='typ')
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='typ2trip_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='typ2trip_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        ordering = ['-id']
        verbose_name = '行程类型二联表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.trip.name) + '-' + str(self.typ.name)
@admin.register(Typ2Trip)
class Typ2TripAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id', 'trip','typ','created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('trip','typ','created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 提供引用查询
    search_fields=('trip__name',)
    list_filter = ('typ__name',)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)

# 行程评论
class TripTalk(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    trip = models.ForeignKey(Trip,  verbose_name='行程',help_text='行程（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    desc = models.CharField(max_length=120, verbose_name='行程评论', help_text='行程评论（CharField）')
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='triptalk_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='triptalk_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        ordering = ['-id']
        verbose_name = '行程评论'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.trip.name
@admin.register(TripTalk)
class TripTalkAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id','trip', 'desc', 'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('trip','created_by','last_edited_by')
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



class TripPraise(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    trip = models.ForeignKey(Trip,  verbose_name='行程',help_text='行程（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='tripp_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='tripp_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        verbose_name = '行程-用户-点赞'
        verbose_name_plural = verbose_name
        unique_together = ('trip', 'created_by',)
@admin.register(TripPraise)
class TripPraiseAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id','trip',  'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('trip', 'created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 设置点击编辑字段
    list_display_links = ( 'id',)
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)


class TripCollect(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    trip = models.ForeignKey(Trip,  verbose_name='行程',help_text='行程（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='tripc_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='tripc_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        verbose_name = '行程-用户-收藏'
        verbose_name_plural = verbose_name
        unique_together = ('trip', 'created_by',)
@admin.register(TripCollect)
class TripCollectAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id','trip',  'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('trip', 'created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 设置点击编辑字段
    list_display_links = ( 'id',)
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)

# 行程添加地点
class PlacesInTrip(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))

    trip = models.ForeignKey(Trip,  verbose_name='行程',help_text='行程（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    place = models.ForeignKey(Place,  verbose_name='地点',help_text='地点（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    index = models.PositiveIntegerField(verbose_name='顺序', help_text='顺序(PositiveIntegerField)', null=True, blank=True)
    
    name = models.CharField(max_length=225, verbose_name='主要事项', help_text='主要事项（CharField）',blank=True)
    desc = models.TextField(verbose_name='备忘', help_text='备忘（TextField）', blank=True)

    theDate = models.DateField(verbose_name='起始日期', help_text='起始日期（DateTimeField）', null=True, blank=True)
    theBegin = models.TimeField(verbose_name='预期起始', help_text='预期起始（DateTimeField）', null=True, blank=True)
    theTime = models.DecimalField( verbose_name='预期时长(h)', help_text='预期时长(h)（PositiveIntegerField）', blank=True, null=True, max_digits=10, decimal_places=1)

    thePay = models.DecimalField( verbose_name='预算(元)', help_text='预算(元)（PositiveIntegerField）', blank=True, null=True, max_digits=10, decimal_places=1)
    
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='pit_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='pit_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')

    class Meta:
        verbose_name = '行程添加地点'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.place
@admin.register(PlacesInTrip)
class PlacesInTripAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id','name','desc','index','place','trip','theDate','theBegin','theTime','thePay', 'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('trip', 'created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 设置点击编辑字段
    list_display_links = ( 'id',)
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)
