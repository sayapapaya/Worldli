# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_problemimage_problem'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='latitude',
            field=models.FloatField(default=b'40.7127837'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='problem',
            name='longitude',
            field=models.FloatField(default=b'-74.0059413'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='problemimage',
            name='image',
            field=models.ImageField(null=True, upload_to=b'img/', blank=True),
            preserve_default=True,
        ),
    ]
