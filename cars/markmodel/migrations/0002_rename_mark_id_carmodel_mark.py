# Generated by Django 4.2.7 on 2023-11-18 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('markmodel', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carmodel',
            old_name='mark_id',
            new_name='mark',
        ),
    ]
