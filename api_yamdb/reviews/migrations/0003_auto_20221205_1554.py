# Generated by Django 2.2.16 on 2022-12-05 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20221205_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Адрес категории', unique=True, verbose_name='Адрес'),
        ),
    ]
