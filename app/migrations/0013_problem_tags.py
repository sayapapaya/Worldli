# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_project_project_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='tags',
            field=models.CharField(default=b'Poverty', max_length=100, choices=[(b'P', b'Pollution'), (b'Poverty', b'Poverty'), (b'First World Problems', b'First World Problems'), (b'Basic Necessities', b'Basic Necessities'), (b'Environment', b'Environment'), (b'Human rights', b'human rights'), (b'social', b'social')]),
            preserve_default=True,
        ),
    ]
