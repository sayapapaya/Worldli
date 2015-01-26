# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_problem_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='founder',
        ),
        migrations.RemoveField(
            model_name='project',
            name='problem',
        ),
        migrations.RemoveField(
            model_name='project_comment',
            name='project',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.RemoveField(
            model_name='project_comment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Project_Comment',
        ),
    ]
