# Generated by Django 3.1.7 on 2021-04-23 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20210423_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactformmessage',
            name='email',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='contactformmessage',
            name='message',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='contactformmessage',
            name='subject',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='contactformmessage',
            name='name',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]