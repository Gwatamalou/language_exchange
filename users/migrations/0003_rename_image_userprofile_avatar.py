# Generated by Django 5.1.1 on 2024-10-05 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_lengthskill_languageskill_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='image',
            new_name='avatar',
        ),
    ]