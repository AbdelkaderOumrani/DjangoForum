# Generated by Django 2.1.7 on 2019-08-22 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]
