# Generated by Django 2.2.6 on 2019-10-09 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20191009_0238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
    ]
