# Generated by Django 2.2.16 on 2021-12-05 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20211205_1135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='title',
            old_name='categories',
            new_name='category',
        ),
    ]