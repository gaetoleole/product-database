# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-17 18:40
from __future__ import unicode_literals

import app.productdb.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('productdb', '0007_auto_20160705_1942'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='unique name for the product list', max_length=2048, unique=True, verbose_name='Product List Name:')),
                ('string_product_list', models.TextField(help_text='Product IDs separated by word wrap or semicolon', max_length=16384, validators=[app.productdb.validators.validate_product_list_string], verbose_name='Unstructured Product ID list:')),
                ('description', models.TextField(blank=True, help_text="short description what's part of this Product List", max_length=4096, null=True, verbose_name='Description:')),
                ('update_date', models.DateField(auto_now=True)),
                ('update_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_lists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='product_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='productdb.ProductGroup', verbose_name='Product Group'),
        ),
    ]
