# Generated by Django 4.0.2 on 2022-04-22 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locallibrary', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
        migrations.AlterModelOptions(
            name='bookreadnow',
            options={'verbose_name': 'Читаю сейчас', 'verbose_name_plural': 'Читаю сейчас'},
        ),
        migrations.AlterModelOptions(
            name='bookwanted',
            options={'verbose_name': 'Хочу прочитать', 'verbose_name_plural': 'Хочу прочитать'},
        ),
    ]
