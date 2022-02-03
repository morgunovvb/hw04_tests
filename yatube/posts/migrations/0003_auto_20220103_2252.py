# Generated by Django 2.2.19 on 2022-01-03 22:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20220103_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='posts.Group'),
        ),
    ]
