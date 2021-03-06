# Generated by Django 3.0.6 on 2020-05-09 11:51

import django.contrib.postgres.fields
from django.db import migrations, models

import apps.attachment.models.attachment


class Migration(migrations.Migration):
    dependencies = [
        ('attachment', '0005_auto_20200507_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='content_type',
            field=models.CharField(choices=[('application/pdf', 'pdf'), ('image/png', 'png'), ('application/zip', 'zip'), ('application/x-rar-compressed', 'rar'), ('application/x-tar', 'tar'), ('application/gzip', 'gz')], default='application/pdf', max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='typeattachment',
            name='allowed_content_types',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('application/pdf', 'pdf'), ('image/png', 'png'), ('application/zip', 'zip'), ('application/x-rar-compressed', 'rar'), ('application/x-tar', 'tar'), ('application/gzip', 'gz')], max_length=64), blank=True, default=apps.attachment.models.attachment._default_allowed_content_types, size=None, verbose_name='List of allowed mime/content types'),
        ),
        migrations.AlterField(
            model_name='typeattachment',
            name='identifier',
            field=models.CharField(choices=[('thesis_text', 'Thesis text'), ('thesis_assigment', 'Thesis assigment'), ('supervisor_review', 'Supervisor review'), ('opponent_review', 'Opponent review'), ('thesis_poster', 'Thesis poster')], max_length=128, unique=True, verbose_name='Identifier'),
        ),
    ]
