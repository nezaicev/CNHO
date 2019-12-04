import re
import os
from typing import NamedTuple
from django.conf import settings
# from main.models import NRusheva
import barcode
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle


def generate_barcode(reg_number):
    EAN = barcode.get_barcode_class('code128')
    data = list(filter(None, re.split('\D', reg_number)))
    data = str(data[0])
    ean = EAN(data, writer=ImageWriter())
    ean.save(settings.BARCODE_MEDIA_ROOT + reg_number, options={
        'module_width': 0.2,
        'module_height': 3,
        'quiet_zone': 0.9,
        'font_size': 10,
        'text_distance': 1.5,
        'background': 'white',
        'foreground': 'black',
        'write_text': True,
        'text': '',
    }, text=None)


def generate_pdf(list, contest_name, reg_number):
    width, height = A4
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Yandex', alignment=TA_JUSTIFY, fontName='Yandex', fontSize=12))
    styles.add(ParagraphStyle(name='YandexBold', alignment=TA_JUSTIFY, fontName='YandexBold', fontSize=12))

    pdfmetrics.registerFont(
        TTFont('Yandex', os.path.join(settings.STATIC_ROOT, 'fonts', 'YandexSansDisplay-Regular.ttf'),
               'YandexBold', os.path.join(settings.STATIC_ROOT, 'fonts', 'static/YandexSansDisplay-Bold.ttf')
               )
    )
    normal_style = styles['Yandex']
    bold_style = styles['Yandex']

    data = [[Paragraph(list[i][0], normal_style), Paragraph(list[i][1], normal_style)] for i in range(0, len(list) - 1)]

    table = Table(data, colWidths=[4 * cm, 14 * cm])

    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    c = canvas.Canvas(os.path.join(settings.MEDIA_ROOT, 'pdf',f'{reg_number}.pdf'), pagesize=A4)
    c.setFont('Yandex', 20)
    c.drawString(20, 810, contest_name)
    c.drawImage(os.path.join(settings.BARCODE_MEDIA_ROOT, f'{reg_number}.png'), 340, 715)

    width2, height2 = table.wrapOn(c, width, height)
    table.drawOn(c, 1.2 * cm, A4[1] - height2 - 125, 0)
    c.save()


# def test_pdf(id_obj):
#     obj = NRusheva.objects.get(id=id_obj)
#     reg_number = obj.reg_number
#     parameters = (
#         ('Конкурс', obj.name),
#         ('Регистрационный №', obj.reg_number),
#         ('Ф.И.О. участника', obj.fio),
#         ('Возраст', obj.get_age_display()),
#         ('Класс', obj.get_level_display()),
#         ('Учебное зав.', obj.school),
#         ('Округ', obj.teacher.get_district_display()),
#         ('Тема работы', obj.get_theme_display()),
#         ('Худ. материалы', obj.get_material_display()),
#         ('Формат работы', obj.get_format_display()),
#         ('Авторское название', obj.author_name),
#         ('Аннотация', obj.description),
#         ('Ф.И.О. педагога', obj.fio_teacher),
#         ('Email педагога', obj.teacher.email)
#     )
#     generate_barcode(obj.reg_number)
#     generate_pdf(parameters, obj.name, reg_number)
# def test_pdf(id_obj):
#     obj = NRusheva.objects.get(id=id_obj)
#     reg_number = obj.reg_number
#     parameters = (
#         'Конкурс', obj.name,
#         'Регистрационный №', obj.reg_number,
#         'Ф.И.О. участника', obj.fio,
#         'Возраст', obj.get_age_display(),
#         'Класс', obj.get_level_display(),
#         'Учебное зав.', obj.school,
#         'Округ', obj.teacher.get_district_display(),
#         'Тема работы', obj.get_theme_display(),
#         'Худ. материалы', obj.get_material_display(),
#         'Формат работы', obj.get_format_display(),
#         'Авторское название', obj.author_name,
#         'Аннотация', obj.description,
#         'Ф.И.О. педагога', obj.fio_teacher,
#         'Email педагога', obj.teacher.email
#     )
#     generate_barcode(obj.reg_number)
#     generate_pdf(parameters, obj.name, reg_number)
