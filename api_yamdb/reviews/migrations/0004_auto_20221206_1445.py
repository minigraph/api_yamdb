# Generated by Django 2.2.16 on 2022-12-06 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20221205_1554'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['slug'], 'verbose_name': 'Категория произведения', 'verbose_name_plural': 'Категории произведений'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['slug'], 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(help_text='Категория', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='reviews.Category', verbose_name='Категория'),
        ),
    ]
