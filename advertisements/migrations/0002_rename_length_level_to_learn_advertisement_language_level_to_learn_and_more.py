# Generated by Django 5.1.1 on 2024-10-05 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='length_level_to_learn',
            new_name='language_level_to_learn',
        ),
        migrations.RenameField(
            model_name='advertisement',
            old_name='length_to_learn',
            new_name='language_to_learn',
        ),
    ]
