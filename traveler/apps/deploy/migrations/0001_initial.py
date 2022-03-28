# Generated by Django 3.0 on 2021-09-23 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0005_auto_20210922_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Swiper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='content（CharField）', max_length=60, verbose_name='content')),
                ('img', models.ImageField(blank=True, help_text='图片（ImageField）', null=True, upload_to='imgs/2021_09', verbose_name='图片')),
                ('path', models.TextField(blank=True, help_text='跳转地址（TextField）', verbose_name='跳转地址')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='创建时间（DateTimeField）', null=True, verbose_name='创建时间')),
                ('last_edited_date', models.DateTimeField(auto_now=True, help_text='最后编辑时间（DateTimeField）', null=True, verbose_name='最后编辑时间')),
                ('deleted', models.CharField(choices=[('0', '未删除'), ('1', '已删除')], default='0', help_text='是否删除（CharField，可选值：0，1）', max_length=1, verbose_name='是否删除')),
                ('created_by', models.ForeignKey(blank=True, help_text='创建人ID（ForeignKey）', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='swiper_cb', to='user.UserExtension', verbose_name='创建人ID')),
                ('last_edited_by', models.ForeignKey(blank=True, help_text='最后编辑人ID（ForeignKey）', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='swiper_eb', to='user.UserExtension', verbose_name='最后编辑人ID')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图',
                'ordering': ['id'],
            },
        ),
    ]