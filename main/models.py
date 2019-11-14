import time
from django.db import models
from main import lists


class Contest(models.Model):
    id = models.AutoField(primary_key=True)
    reg_number = models.IntegerField()
    fio = models.CharField('ФИО участника', max_length=40, blank=True)
    age = models.CharField('Возраст', choices=lists.AGE, max_length=2, blank=True)
    gender = models.CharField(max_length=1, choices=(('M', 'M'), ('Ж', 'Ж')), verbose_name='Пол', blank=True)
    title = models.CharField('Название работы', max_length=100, blank=True)
    date_reg = models.DateTimeField(auto_now=True, blank=True)
    fio_teacher=models.CharField('ФИО Педагога', max_length=40, blank=True)

    def save(self, *args, **kwargs):
        self.reg_number = int(time.time())
        super(Contest, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Teacher(models.Model):
    fio = models.CharField('ФИО педагога', max_length=40, blank=False)
    school = models.CharField('Образовательная организация', max_length=150, blank=False)
    position = models.CharField('Должность', max_length=100, blank=False)
    region = models.CharField('Регион', max_length=101, blank=False)
    city = models.CharField('Населенный пункт', max_length=101, blank=True)
    district = models.CharField('Округ', max_length=101, blank=True)
    email = models.EmailField('email', blank=False, unique=True)
    phone = models.CharField('Телефон', max_length=15, blank=True)
    age = models.CharField('Возрастная категория', max_length=30, blank=True)


class Child(models.Model):
    fio = models.CharField('ФИО участника', max_length=40, blank=True)
    region = models.CharField('Регион', max_length=101, blank=True)
    district = models.CharField('Округ', max_length=101, blank=True)
    city = models.CharField('Город', max_length=101, blank=True)
    school = models.CharField('Образовательное учреждение', max_length=150, blank=True)
    birth_date = models.DateField(blank=True)
    email = models.EmailField('email', blank=True)


class Mskch(Contest):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

class Artakiada(Contest):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)