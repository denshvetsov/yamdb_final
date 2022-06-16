# Generated by Django 2.2.16 on 2022-05-13 05:54

import catalog.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('slug', models.SlugField(default='empty', unique=True)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('slug', models.SlugField(default='empty', unique=True)),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('year', models.IntegerField(db_index=True, validators=[catalog.validators.validate_year], verbose_name='Год издания')),
                ('description', models.TextField(blank=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_titles', to='catalog.Category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(related_name='genre_titles', to='catalog.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произвдение',
                'verbose_name_plural': 'Произведения',
                'ordering': ('-id',),
            },
        ),
    ]
