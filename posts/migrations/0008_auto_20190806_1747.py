# Generated by Django 2.1.7 on 2019-08-06 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20190806_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(default='img/avatars/empty.png', upload_to='img/avatars'),
        ),
    ]
