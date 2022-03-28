# Generated by Django 3.0 on 2021-09-26 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_auto_20210923_0935'),
        ('place', '0002_place_show'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='img1',
            field=models.ForeignKey(blank=True, help_text='图片（ForeignKey）', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='place_img1', to='files.Images', verbose_name='图片1'),
        ),
        migrations.AddField(
            model_name='place',
            name='img2',
            field=models.ForeignKey(blank=True, help_text='图片（ForeignKey）', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='place_img2', to='files.Images', verbose_name='图片2'),
        ),
        migrations.AddField(
            model_name='place',
            name='img3',
            field=models.ForeignKey(blank=True, help_text='图片（ForeignKey）', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='place_img3', to='files.Images', verbose_name='图片3'),
        ),
        migrations.AddField(
            model_name='place',
            name='img4',
            field=models.ForeignKey(blank=True, help_text='图片（ForeignKey）', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='place_img4', to='files.Images', verbose_name='图片4'),
        ),
        migrations.AddField(
            model_name='place',
            name='img5',
            field=models.ForeignKey(blank=True, help_text='图片（ForeignKey）', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='place_img5', to='files.Images', verbose_name='图片5'),
        ),
        migrations.AddField(
            model_name='place',
            name='img6',
            field=models.ForeignKey(blank=True, help_text='图片（ForeignKey）', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='place_img6', to='files.Images', verbose_name='图片6'),
        ),
        migrations.AddField(
            model_name='place',
            name='img7',
            field=models.ForeignKey(blank=True, help_text='图片（ForeignKey）', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='place_img7', to='files.Images', verbose_name='图片7'),
        ),
        migrations.AddField(
            model_name='place',
            name='img8',
            field=models.ForeignKey(blank=True, help_text='图片（ForeignKey）', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='place_img8', to='files.Images', verbose_name='图片8'),
        ),
        migrations.AddField(
            model_name='place',
            name='img9',
            field=models.ForeignKey(blank=True, help_text='图片（ForeignKey）', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='place_img9', to='files.Images', verbose_name='图片9'),
        ),
    ]