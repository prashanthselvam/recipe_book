# Generated by Django 2.2.6 on 2019-10-13 17:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20191013_1701'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipesteps',
            options={'ordering': ('recipe', 'step_number'), 'verbose_name_plural': 'recipe steps'},
        ),
        migrations.AddField(
            model_name='recipesteps',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]