# Generated by Django 4.2.7 on 2023-12-06 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='followers_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='following_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='post_count',
            field=models.IntegerField(default=0),
        ),
    ]
