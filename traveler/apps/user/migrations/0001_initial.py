# Generated by Django 3.0 on 2021-09-18 07:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Portrait',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portrait', models.ImageField(blank=True, help_text='头像（ImageField）', upload_to='img/user/portrait', verbose_name='头像')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='创建时间（DateTimeField）', null=True, verbose_name='创建时间')),
                ('last_edited_date', models.DateTimeField(auto_now=True, help_text='最后编辑时间（DateTimeField）', null=True, verbose_name='最后编辑时间')),
                ('deleted', models.CharField(choices=[('0', '未删除'), ('1', '已删除')], default='0', help_text='是否删除（CharField，可选值：0，1）', max_length=1, verbose_name='是否删除')),
            ],
            options={
                'verbose_name': '肖像图片',
                'verbose_name_plural': '肖像图片',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TelCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone', models.CharField(blank=True, help_text='电话（CharField）', max_length=20, unique=True, verbose_name='电话')),
                ('code', models.CharField(blank=True, help_text='验证码（CharField）', max_length=10, verbose_name='验证码')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='创建时间（DateTimeField）', null=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '验证码对应',
                'verbose_name_plural': '验证码对应',
            },
        ),
        migrations.CreateModel(
            name='UserExtension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realname', models.CharField(blank=True, help_text='真实姓名（CharField）', max_length=30, verbose_name='真实姓名')),
                ('desc', models.CharField(blank=True, help_text='个性签名（CharField）', max_length=120, verbose_name='个性签名')),
                ('project', models.TextField(blank=True, help_text='可见模块（TextField）', verbose_name='可见项目')),
                ('modules', models.TextField(blank=True, help_text='可见模块（TextField）', verbose_name='可见模块')),
                ('sex', models.CharField(blank=True, choices=[('0', '男'), ('1', '女')], default='0', help_text='性别（CharField，可选值：0，1）', max_length=1, verbose_name='性别')),
                ('telephone', models.CharField(blank=True, help_text='电话（CharField）', max_length=20, unique=True, verbose_name='电话')),
                ('birthday', models.DateField(blank=True, help_text='生日（DateField）', null=True, verbose_name='生日')),
                ('visits', models.PositiveIntegerField(blank=True, default=0, help_text='访问次数（PositiveIntegerField）', null=True, verbose_name='访问次数')),
                ('portrait', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Portrait', verbose_name='用户头像')),
                ('user', models.OneToOneField(help_text='用户ID（OneToOneField）', on_delete=django.db.models.deletion.CASCADE, related_name='extension', to=settings.AUTH_USER_MODEL, verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
        migrations.AddField(
            model_name='portrait',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='创建人ID（ForeignKey）', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='portrait_cb', to='user.UserExtension', verbose_name='创建人ID'),
        ),
        migrations.AddField(
            model_name='portrait',
            name='last_edited_by',
            field=models.ForeignKey(blank=True, help_text='最后编辑人ID（ForeignKey）', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='portrait_eb', to='user.UserExtension', verbose_name='最后编辑人ID'),
        ),
    ]