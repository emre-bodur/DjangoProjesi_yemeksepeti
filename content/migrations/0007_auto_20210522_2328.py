# Generated by Django 3.1.7 on 2021-05-22 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_auto_20210522_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='level',
        ),
        migrations.RemoveField(
            model_name='content',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='content',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='content',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='content',
            name='tree_id',
        ),
    ]
