# Generated by Django 3.0.6 on 2020-05-09 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('thesis', '0011_auto_20200429_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesis',
            name='opponent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='thesis_opponent', to=settings.AUTH_USER_MODEL, verbose_name='Opponent'),
        ),
    ]
