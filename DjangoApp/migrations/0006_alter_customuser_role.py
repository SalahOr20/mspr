# Generated by Django 4.2.6 on 2024-07-04 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoApp', '0005_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('owner', 'Owner'), ('botanist', 'Botanist')], default='owner', max_length=10),
        ),
    ]