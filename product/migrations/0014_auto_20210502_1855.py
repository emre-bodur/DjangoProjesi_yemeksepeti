# Generated by Django 3.1.7 on 2021-05-02 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_auto_20210502_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
