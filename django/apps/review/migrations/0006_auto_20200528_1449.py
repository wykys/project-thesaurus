# Generated by Django 3.0.6 on 2020-05-28 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thesis', '0022_auto_20200528_1449'),
        ('review', '0005_auto_20200518_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='thesis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_thesis', to='thesis.Thesis'),
        ),
    ]
