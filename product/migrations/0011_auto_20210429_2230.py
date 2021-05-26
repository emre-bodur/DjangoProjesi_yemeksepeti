# Generated by Django 3.1.7 on 2021-04-29 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20210429_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('New', 'Yeni'), ('False', 'Hayır'), ('False', 'Hayır')], default='New', max_length=10),
        ),
    ]