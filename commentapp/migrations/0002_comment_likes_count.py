# Generated by Django 4.2.7 on 2023-12-12 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commentapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes_count',
            field=models.IntegerField(default=0),
        ),
    ]