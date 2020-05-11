# Generated by Django 3.0.5 on 2020-04-29 21:38
from typing import Type

from django.contrib.auth.models import Group
from django.db import migrations
from django.db.migrations import RunPython


def create_groups(apps, schema_editor):
    group = apps.get_model('auth', 'Group')  # type: Type[Group]

    group.objects.get_or_create(name='student')
    group.objects.get_or_create(name='teacher')
    group.objects.get_or_create(name='manager')


def remove_groups(apps, schema_editor):
    group = apps.get_model('auth', 'Group')  # type: Type[Group]

    group.objects.filter(name__in='student teacher manager'.split()).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0003_auto_20200425_1602'),
    ]

    operations = [
        RunPython(create_groups, remove_groups)
    ]
