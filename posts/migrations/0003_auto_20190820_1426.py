# Generated by Django 2.1.7 on 2019-08-20 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20190820_1412'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='cover',
            new_name='image',
        ),
    ]