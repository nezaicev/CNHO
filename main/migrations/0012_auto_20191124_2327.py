# Generated by Django 2.2.7 on 2019-11-24 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20191119_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artakiada',
            name='age',
        ),
        migrations.RemoveField(
            model_name='artakiada',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='artakiada',
            name='title',
        ),
        migrations.AddField(
            model_name='artakiada',
            name='city',
            field=models.CharField(blank=True, max_length=101, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='artakiada',
            name='district',
            field=models.CharField(blank=True, max_length=101, verbose_name='Округ'),
        ),
        migrations.AddField(
            model_name='artakiada',
            name='email',
            field=models.EmailField(default=1, max_length=254, verbose_name='email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artakiada',
            name='level',
            field=models.CharField(choices=[('0', 'Дошкольник'), ('1', '1 класс'), ('2', '2 класс'), ('3', '3 класс'), ('4', '4 класс'), ('5', '5 класс'), ('6', '6 класс'), ('7', '7 класс'), ('8', '8 класс'), ('9', '9 класс'), ('10', '10 класс'), ('11', '11 класс')], default=1, max_length=2, verbose_name='Класс'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artakiada',
            name='region',
            field=models.CharField(blank=True, max_length=101, verbose_name='Регион'),
        ),
        migrations.AddField(
            model_name='artakiada',
            name='school',
            field=models.CharField(default=1, max_length=150, verbose_name='Образовательная организация'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artakiada',
            name='status',
            field=models.CharField(blank=True, choices=[('0', 'Новый уч. 1-тура'), ('1', 'Просмотрен'), ('2', 'Участник 2-тура'), ('3', 'Участник 2-отбор'), ('4', 'Победитель 1 - место'), ('5', 'Призер 2 - место'), ('6', 'Призер 3 - место')], max_length=2, verbose_name='Статус участника'),
        ),
        migrations.DeleteModel(
            name='Mskch',
        ),
    ]
