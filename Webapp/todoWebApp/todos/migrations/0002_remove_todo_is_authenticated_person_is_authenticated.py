# Generated by Django 4.0.6 on 2022-08-19 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='is_authenticated',
        ),
        migrations.AddField(
            model_name='person',
            name='is_authenticated',
            field=models.BooleanField(default=False),
        ),
    ]
