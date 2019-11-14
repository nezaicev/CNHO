# Generated by Django 2.2.7 on 2019-11-14 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20191113_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mskch',
            name='name_contest',
        ),
        migrations.RemoveField(
            model_name='mskch',
            name='nomination',
        ),
        migrations.RemoveField(
            model_name='mskch',
            name='reg_number',
        ),
        migrations.AddField(
            model_name='mskch',
            name='age',
            field=models.CharField(blank=True, choices=[('5', '5 лет'), ('6', '6 лет'), ('7', '7 лет'), ('8', '8 лет'), ('9', '9 лет'), ('10', '10 лет'), ('11', '11 лет'), ('12', '12 лет'), ('13', '13 лет'), ('14', '14 лет'), ('15', '15 лет'), ('16', '16 лет'), ('17', '17 лет'), ('18', '18 лет')], max_length=2, verbose_name='Возраст'),
        ),
        migrations.AddField(
            model_name='mskch',
            name='fio',
            field=models.CharField(blank=True, max_length=40, verbose_name='ФИО участника'),
        ),
        migrations.AddField(
            model_name='mskch',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'M'), ('Ж', 'Ж')], max_length=1, verbose_name='Пол'),
        ),
    ]
