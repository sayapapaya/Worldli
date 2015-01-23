# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20150119_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='solution',
        ),
        migrations.AddField(
            model_name='comment',
            name='followup',
            field=models.ForeignKey(default=None, to='app.Comment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='problem',
            field=models.ForeignKey(default=1, to='app.Problem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='upvotes',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
