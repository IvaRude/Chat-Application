# Generated by Django 4.0.3 on 2022-05-17 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userinfo_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='first_name',
            field=models.CharField(default='', max_length=30, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='last_name',
            field=models.CharField(default='', max_length=30, verbose_name='Фамилия'),
        ),
    ]
