# Generated by Django 4.2.6 on 2024-04-30 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='id_user',
            new_name='id',
        ),
    ]
