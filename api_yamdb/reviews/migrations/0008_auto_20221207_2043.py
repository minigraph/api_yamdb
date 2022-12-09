# Generated by Django 2.2.16 on 2022-12-07 20:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_merge_20221207_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genresoftitles',
            name='genre',
            field=models.ForeignKey(help_text='Жанр', on_delete=django.db.models.deletion.CASCADE, to='reviews.Genre', verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='genresoftitles',
            name='title',
            field=models.ForeignKey(help_text='Произведение', on_delete=django.db.models.deletion.CASCADE, to='reviews.Title', verbose_name='Произведение'),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(help_text='Категория', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='titles', through='reviews.GenresOfTitles', to='reviews.Genre'),
        ),
    ]
