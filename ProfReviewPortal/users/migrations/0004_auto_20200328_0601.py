# Generated by Django 3.0.4 on 2020-03-28 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200328_0532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ban',
            name='end',
            field=models.DateField(null=True),
        ),
    ]
