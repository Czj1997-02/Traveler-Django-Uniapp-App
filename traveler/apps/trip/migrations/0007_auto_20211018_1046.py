# Generated by Django 3.0 on 2021-10-18 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0006_auto_20211014_1442'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='triptalk',
            options={'ordering': ['-id'], 'verbose_name': '行程评论', 'verbose_name_plural': '行程评论'},
        ),
    ]
