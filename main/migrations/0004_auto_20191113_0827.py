# Generated by Django 2.2.7 on 2019-11-13 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20191108_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email'),
        ),
    ]