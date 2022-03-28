from django.db import models

# Create your models here.
# 地点词条
# 地点词条评论
from django.contrib import admin
from user.models import UserExtension
from mdeditor.fields import MDTextField
from django.utils.timezone import now
from files.models import Images
from user.models import City
# Create your models here.
# 地点词条
class Place(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    typ_choices = ( ('play', '景玩'),('eat', '餐食'),('hotel', '住宿'),('go', '出行'),('other', '其他'))
    gaode = models.CharField(max_length=225, verbose_name='地点词条高德链接', help_text='地点词条高德链接（CharField）',blank=True)
    lng = models.DecimalField( verbose_name='经度', help_text='经度（PositiveIntegerField）', blank=True, null=True, max_digits=30, decimal_places=20)
    lat = models.DecimalField( verbose_name='纬度', help_text='纬度（PositiveIntegerField）', blank=True, null=True, max_digits=30, decimal_places=20)

    img1 = models.ForeignKey(Images,  verbose_name='图片1',help_text='图片（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='place_img1')
    img2 = models.ForeignKey(Images,  verbose_name='图片2',help_text='图片（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='place_img2')
    img3 = models.ForeignKey(Images,  verbose_name='图片3',help_text='图片（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='place_img3')
    img4 = models.ForeignKey(Images,  verbose_name='图片4',help_text='图片（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='place_img4')
    img5 = models.ForeignKey(Images,  verbose_name='图片5',help_text='图片（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='place_img5')
    img6 = models.ForeignKey(Images,  verbose_name='图片6',help_text='图片（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='place_img6')
    img7 = models.ForeignKey(Images,  verbose_name='图片7',help_text='图片（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='place_img7')
    img8 = models.ForeignKey(Images,  verbose_name='图片8',help_text='图片（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='place_img8')
    img9 = models.ForeignKey(Images,  verbose_name='图片9',help_text='图片（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='place_img9')

    name = models.CharField(max_length=225, verbose_name='地点词条名称', help_text='地点词条名称（CharField）')
    desc = MDTextField(verbose_name="地点词条内容", blank=True)
    typ = models.CharField(max_length=10, verbose_name='词条分类', help_text='词条分类（CharField，可选值：play,eat,hotel,go）', choices=typ_choices, default='play', blank=True)
    city = models.ForeignKey(City, verbose_name='城市', null=True, blank=True, on_delete=models.SET_NULL,related_name='place_city')

    show = models.BooleanField(verbose_name='是否公开可见',help_text='是否公开可见',default=True)
    editedDay = models.DateField(verbose_name='编辑日期', help_text='编辑日期（DateTimeField）', auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='place_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='place_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        ordering = ['-id']
        verbose_name = '地点词条'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
@admin.register(Place)
class PlaceAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id', 'name','gaode','lng','lat','img1','img2','img3','img4','img5','img6','img7','img8','img9','desc','typ','city','show','editedDay','created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 提供引用查询
    search_fields=('name',)
    list_filter = ('name','typ')
    # 设置点击编辑字段
    list_display_links = ( 'id','name',)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)

# 地点词条类型
class PlaceType(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    name = models.CharField(max_length=60, verbose_name='地点词条类型', help_text='地点词条类型（CharField）')
    color = models.CharField(max_length=60, verbose_name='标签颜色', help_text='标签颜色（CharField）',default='#6190e8')
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='placet_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='placet_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        verbose_name = '地点词条类型'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
@admin.register(PlaceType)
class PlaceTypeAdminModel(admin.ModelAdmin):
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

# 地点词条类型二联表
class Typ2Place(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    place = models.ForeignKey(Place,  verbose_name='地点词条',help_text='地点词条（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    typ = models.ForeignKey(PlaceType,  verbose_name='地点词条类别',help_text='地点词条类别（ForeignKey）', null=True, blank=True, on_delete=models.SET_NULL, related_name='typ')
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='typ2place_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='typ2place_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        ordering = ['-id']
        verbose_name = '地点词条类型二联表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.place.name) + '-' + str(self.typ.name)
@admin.register(Typ2Place)
class Typ2PlaceAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id', 'place','typ','created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('place','typ','created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 提供引用查询
    search_fields=('place__name',)
    list_filter = ('typ__name',)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)

# 地点词条评论
class PlaceTalk(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    place = models.ForeignKey(Place,  verbose_name='地点词条',help_text='地点词条（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    desc = models.CharField(max_length=120, verbose_name='地点词条评论', help_text='地点词条评论（CharField）')
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='placetalk_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='placetalk_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        ordering = ['-id']
        verbose_name = '地点词条评论'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.place.name
@admin.register(PlaceTalk)
class PlaceTalkAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id','place', 'desc', 'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('place','created_by','last_edited_by')
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





class PlacePraise(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    place = models.ForeignKey(Place,  verbose_name='地点',help_text='地点（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='placep_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='placep_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        verbose_name = '地点-用户-点赞'
        verbose_name_plural = verbose_name
        unique_together = ('place', 'created_by',)
@admin.register(PlacePraise)
class PlacePraiseAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id','place',  'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('place', 'created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 设置点击编辑字段
    list_display_links = ( 'id',)
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)


class PlaceCollect(models.Model):
    del_choices = ( ('0', '未删除'),('1', '已删除'))
    place = models.ForeignKey(Place,  verbose_name='地点',help_text='地点（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserExtension,  verbose_name='创建人ID',help_text='创建人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='placec_cb')
    created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
    last_edited_by = models.ForeignKey(UserExtension,  verbose_name='最后编辑人ID',help_text='最后编辑人ID（ForeignKey）', null=True, blank=True, on_delete=models.CASCADE, related_name='placec_eb')
    last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
    deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')
    class Meta:
        verbose_name = '地点-用户-收藏'
        verbose_name_plural = verbose_name
        unique_together = ('place', 'created_by',)
@admin.register(PlaceCollect)
class PlaceCollectAdminModel(admin.ModelAdmin):
    # 添加分页
    list_per_page = 50
    # 列表页展示的字段
    list_display = ('id','place',  'created_by', 'created_date', 'last_edited_by','last_edited_date')
    # 使用到外键下拉的字段
    autocomplete_fields = ('place', 'created_by','last_edited_by')
    # 开放操作动作
    actions_on_bottom = True
    # 设置点击编辑字段
    list_display_links = ( 'id',)
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.extension
        obj.last_edited_by = request.user.extension
        super().save_model(request, obj, form, change)