# Generated by Django 2.2.1 on 2020-03-26 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20200324_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
