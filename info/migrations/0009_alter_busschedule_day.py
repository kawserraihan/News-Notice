# Generated by Django 4.2.5 on 2023-12-17 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0008_busschedule_route_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busschedule',
            name='day',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
