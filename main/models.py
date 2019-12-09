import time
from django.db import models
from main import lists, utils


class Contest(models.Model):
    id = models.AutoField(primary_key=True)
    reg_number = models.CharField(max_length=15, blank=False, null=False)
    date_reg = models.DateTimeField(auto_now=True, blank=True)
    school = models.CharField('Образовательная организация', max_length=150, blank=False)
    fio = models.CharField('ФИО участника', max_length=500, blank=False)
    fio_teacher = models.CharField('ФИО Педагога', max_length=500, blank=False)
    email = models.EmailField('email', blank=False)
    status = models.CharField(max_length=2, choices=lists.STATUS, blank=True, verbose_name='Статус участника')
    region = models.CharField('Регион', max_length=101, blank=True)
    city = models.CharField('Город', max_length=101, blank=True)
    district = models.CharField('Округ', max_length=101, blank=True)

    def save(self, *args, **kwargs):
        self.reg_number = int(time.time())
        super(Contest, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Teacher(models.Model):
    fio = models.CharField('ФИО педагога', max_length=40, blank=False)
    school = models.CharField('Образовательная организация', max_length=150, blank=True)
    position = models.CharField('Должность', choices=lists.POSITIONS, max_length=100, blank=True)
    region = models.CharField('Регион', choices=lists.REGIONS, max_length=101, blank=True)
    city = models.CharField('Населенный пункт', max_length=101, blank=True)
    district = models.CharField('Округ', choices=lists.DISTRICT, max_length=101, blank=True)
    email = models.EmailField('email', blank=False, unique=True)
    phone = models.CharField('Телефон', max_length=15, blank=True)
    age = models.CharField('Возрастная категория', choices=lists.AGE_TEACHER, max_length=30, blank=True)
    status = models.CharField('Статус', max_length=10, choices=lists.REG_STATUS, blank=False)
    info = models.CharField(max_length=100, blank=True)


class Artakiada(Contest):
    full_name = 'АРТакиада "Изображение и слово"'
    name = 'АРТакиада "Изображение и слово"'

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    level = models.CharField(max_length=2, choices=lists.LEVEL, blank=False, verbose_name='Класс')

    def get_parm_for_pdf(self):
        parameters = (
            ('Конкурс', self.name),
            ('Регистрационный №', self.reg_number),
            ('Ф.И.О. участника', self.fio),
            ('Учебное зав.', self.school),
            ('Класс', self.get_level_display()),
            ('Регион', self.teacher.get_region_display()),
            ('Город', self.teacher.city),
            ('Округ', self.teacher.get_district_display()),
            ('Ф.И.О. педагога', self.fio_teacher),
            ('Email педагога', self.teacher.email)
        )
        return parameters


class NRusheva(Contest):
    full_name = 'Московский городской конкурс детского рисунка имени Нади Рушевой'
    name = 'Конкурс им. Нади Рушевой'

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    level = models.CharField(max_length=2, choices=lists.LEVEL, blank=False, verbose_name='Класс')
    age = models.CharField(max_length=2, choices=lists.AGE, blank=False, verbose_name='Возраст')
    gender = models.CharField(max_length=1, choices=(('M', 'M'), ('Ж', 'Ж')), verbose_name='Пол')
    theme = models.CharField(max_length=2, choices=lists.THEME, blank=False, verbose_name='Тема работы')
    material = models.CharField(max_length=50, blank=False, choices=lists.MATERIAL, verbose_name='Худ. материалы')
    author_name = models.CharField(max_length=50, blank=False, verbose_name='Авторское название')
    format = models.CharField(max_length=2, choices=lists.FORMAT, blank=False, verbose_name='Формат работы')
    description = models.TextField(max_length=500, blank=False, verbose_name='Аннотация')
    image = models.ImageField(upload_to='images/', null=True, blank=False)

    def get_parm_for_pdf(self):
        parameters = (
            ('Конкурс', self.name),
            ('Регистрационный №', self.reg_number),
            ('Ф.И.О. участника', self.fio),
            ('Возраст', self.get_age_display()),
            ('Класс', self.get_level_display()),
            ('Учебное зав.', self.school),
            ('Округ', self.teacher.get_district_display()),
            ('Тема работы', self.get_theme_display()),
            ('Худ. материалы', self.get_material_display()),
            ('Формат работы', self.get_format_display()),
            ('Авторское название', self.author_name),
            ('Аннотация', self.description),
            ('Ф.И.О. педагога', self.fio_teacher),
            ('Email педагога', self.teacher.email)
        )
        return parameters


class Mymoskvichi(Contest):
    full_name = 'Московский городской конурс "Мы Москвичи"'
    name = 'Конкурс "Мы Москвичи"'

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    theme = models.CharField(max_length=2, choices=lists.THEME, blank=False, verbose_name='Номинация')
    author_name = models.CharField(max_length=50, blank=False, verbose_name='Авторское название')
