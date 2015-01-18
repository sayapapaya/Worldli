# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150117_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'')),
                ('problem', models.ForeignKey(to='app.Problem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
