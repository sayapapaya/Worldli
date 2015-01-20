# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_problemimage_problem'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemimage',
            name='problem',
            field=models.ForeignKey(default=1, to='app.Problem'),
            preserve_default=False,
        ),
    ]
