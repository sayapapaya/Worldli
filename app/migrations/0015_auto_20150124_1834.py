# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20150124_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='tags',
            field=models.CharField(default=b'Poverty', max_length=100),
            preserve_default=True,
        ),
    ]
