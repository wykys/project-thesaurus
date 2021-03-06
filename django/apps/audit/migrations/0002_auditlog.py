# Generated by Django 3.0.6 on 2020-05-29 22:06

import django.contrib.postgres.fields.hstore
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('audit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('event_id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('schema_name', models.CharField(max_length=64, verbose_name='Schema name')),
                ('table_name', models.CharField(max_length=64, verbose_name='Table name')),
                ('action_tstamp_tx', models.DateTimeField(verbose_name='Transaction start timestamp')),
                ('action_tstamp_stm', models.DateTimeField(verbose_name='Statement start timestamp')),
                ('action_tstamp_clk', models.DateTimeField(verbose_name='Wall clock time')),
                ('transaction_id', models.BigIntegerField(verbose_name='Transaction ID')),
                ('client_query', models.TextField(verbose_name='Client query')),
                ('action', models.CharField(choices=[('I', 'Inserted'), ('D', 'Deleted'), ('U', 'Updated'), ('T', 'Truncated')], max_length=1, verbose_name='Action')),
                ('row_data', django.contrib.postgres.fields.hstore.HStoreField(null=True, verbose_name='Row data')),
                ('changed_fields', django.contrib.postgres.fields.hstore.HStoreField(null=True, verbose_name='Changed fields')),
                ('statement_only', models.BooleanField(verbose_name='Statement only')),
            ],
            options={
                'verbose_name': 'Audit',
                'verbose_name_plural': 'Audit',
                'db_table': 'logged_actions',
                'ordering': ['-action_tstamp_clk'],
                'managed': False,
            },
        ),
    ]
