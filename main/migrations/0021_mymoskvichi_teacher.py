# Generated by Django 2.2.7 on 2019-11-27 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_mymoskvichi'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymoskvichi',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Teacher'),
        ),
    ]
