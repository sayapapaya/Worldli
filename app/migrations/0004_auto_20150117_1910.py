# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_problemimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='country',
            new_name='location',
        ),
        migrations.AlterField(
            model_name='problemimage',
            name='image',
            field=models.ImageField(null=True, upload_to=b'../static/img/', blank=True),
            preserve_default=True,
        ),
    ]
