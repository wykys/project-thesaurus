# Generated by Django 3.0.6 on 2020-05-29 16:43

from django.db import migrations

from apps.audit.operations import EnableAuditOperation


class Migration(migrations.Migration):
    dependencies = [
        ('attachment', '0010_attachment_size'),
    ]

    operations = [
        EnableAuditOperation('Attachment'),
    ]
