# Generated by Django 4.2.7 on 2023-11-30 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_image',
            field=models.ImageField(blank=True, null=True, upload_to='postpic'),
        ),
    ]
