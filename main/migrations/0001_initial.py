# Generated by Django 2.2.7 on 2019-11-07 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=40, verbose_name='ФИО участника')),
                ('region', models.CharField(max_length=101, verbose_name='Регион')),
                ('district', models.CharField(max_length=101, verbose_name='Округ')),
                ('city', models.CharField(max_length=101, verbose_name='Город')),
                ('school', models.CharField(max_length=150, verbose_name='Образовательное учреждение')),
                ('birth_date', models.DateField()),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
            ],
        ),
        migrations.CreateModel(
            name='Mskch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reg_number', models.IntegerField(unique=True, verbose_name='Регистрационный номер')),
                ('nomination', models.CharField(max_length=100, verbose_name='Номинация')),
                ('name_contest', models.CharField(max_length=100, verbose_name='Название конкурса')),
                ('title', models.CharField(max_length=100, verbose_name='Название работы')),
                ('date_reg', models.DateField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=40, verbose_name='ФИО педагога')),
                ('region', models.CharField(max_length=101, verbose_name='Регион')),
                ('district', models.CharField(max_length=101, verbose_name='Округ')),
                ('city', models.CharField(max_length=101, verbose_name='Город')),
                ('school', models.CharField(max_length=150, verbose_name='Образовательное учреждение')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('phone', models.CharField(max_length=15, verbose_name='Телефон')),
                ('experience', models.CharField(max_length=10, verbose_name='Стаж')),
            ],
        ),
    ]