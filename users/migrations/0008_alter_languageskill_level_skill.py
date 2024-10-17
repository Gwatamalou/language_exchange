# Generated by Django 5.1.1 on 2024-10-17 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_languageskill_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languageskill',
            name='level_skill',
            field=models.CharField(choices=[('начальный', 'начальный'), ('ниже среднего', 'ниже среднего'), ('средний', 'средний'), ('выше среднего', 'выше среднего'), ('продвинутый', 'продвинутый'), ('профессиональный', 'профессиональный')], help_text='Выберите язык, на котором вы хотите работать.', max_length=30),
        ),
    ]
