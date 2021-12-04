# Generated by Django 2.2.16 on 2021-12-03 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('moderator', 'm'), ('admin', 'a'), ('user', 'u')], max_length=20, verbose_name='Статус пользователя'),
        ),
    ]
