from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class Contest(models.Model):
    id = models.AutoField(primary_key=True)
    reg_number = models.IntegerField('Регистрационный номер', unique=True)
    nomination = models.CharField('Номинация', max_length=100)
    name_contest = models.CharField('Название конкурса', max_length=100)
    title = models.CharField('Название работы', max_length=100)
    date_reg = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Teacher(models.Model):
    fio = models.CharField('ФИО педагога', max_length=40)
    region = models.CharField('Регион', max_length=101)
    district = models.CharField('Округ', max_length=101)
    city = models.CharField('Город', max_length=101)
    school = models.CharField('Образовательное учреждение', max_length=150)
    email = models.EmailField('email')
    phone = models.CharField('Телефон', max_length=15)
    experience = models.CharField('Стаж', max_length=10)


class Child(models.Model):
    fio = models.CharField('ФИО участника', max_length=40)
    region = models.CharField('Регион', max_length=101)
    district = models.CharField('Округ', max_length=101)
    city = models.CharField('Город', max_length=101)
    school = models.CharField('Образовательное учреждение', max_length=150)
    birth_date = models.DateField()
    email = models.EmailField('email')
