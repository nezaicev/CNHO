import re
import os
import time
from datetime import date
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
import barcode
import xlwt
from PIL import Image, ExifTags
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
from main import lists


def generate_xls(queryset,field_names,exclude_field,path):

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(field_names)):
        ws.write(row_num, col_num, field_names[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    for ridx, obj in enumerate(queryset):
        ridx += 1
        for cidx, field in enumerate(obj._meta.fields):
            if field.name not in exclude_field:
                if field.choices:
                    val = obj._get_FIELD_display(field)
                    ws.write(ridx, cidx, val, font_style)
                else:
                    val = getattr(obj, field.name)
                    ws.write(ridx, cidx, val, font_style)

    wb.save(path)


def generate_report(model):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename={}.xls'.format(model._meta)

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Stat')

    # Sheet header, first row
    row_num = 0
    list_district = [i for i in range(1, lists.DISTRICT.__len__() + 1)]
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ws.write(row_num, 1, 'Общее кол-во', font_style)
    ws.write(row_num, 2, 'Участник 2 тура (кол-во)', font_style)
    ws.write(row_num, 3, 'Призер 2 тура (кол-во)', font_style)
    ws.write(row_num, 4, 'Победитель 2 тура (кол-во)', font_style)
    ws.write(row_num, 5, 'Без статуса (кол-во)', font_style)
    ws.write(row_num, 6, '1-4 класс (кол-во)', font_style)
    ws.write(row_num, 7, '5-8 класс (кол-во)', font_style)
    row_num += 1

    for rindx, district in enumerate(lists.DISTRICT):
        row_num+=1
        ws.write(row_num, 0, district[1], font_style)
        ws.write(row_num, 1, model.objects.filter(district=district[0]).count(), font_style)
        ws.write(row_num, 2, model.objects.filter(district=district[0], status=2).count(), font_style)
        ws.write(row_num, 3, model.objects.filter(district=district[0], status=3).count(), font_style)
        ws.write(row_num, 4, model.objects.filter(district=district[0], status=4).count(), font_style)
        ws.write(row_num, 5, model.objects.filter(district=district[0], status='').count(), font_style)
        ws.write(row_num, 6, model.objects.filter(district=district[0],
                                                level__in=[0, 1, 2, 3, 4]).count(),font_style)
        ws.write(row_num, 7, model.objects.filter(district=district[0],
                                                level__in=[5, 6, 7, 8]).count(),font_style)
        # row_num = rindx
    row_num+=3
    ws.write(row_num, 0, 'Общее колличество участников: ', font_style)
    ws.write(row_num , 1, model.objects.all().count(), font_style)
    row_num+=1
    ws.write(row_num, 0, 'Москва', font_style)
    ws.write(row_num, 1, model.objects.filter(region=77).count(), font_style)
    row_num += 1
    ws.write(row_num, 0, 'Моская обл.', font_style)
    ws.write(row_num, 1, model.objects.filter(region=50).count(), font_style)
    row_num += 1
    ws.write(row_num, 0, 'Регионы', font_style)
    ws.write(row_num, 1, model.objects.exclude(region__in=[77, 50]).count(), font_style)
    row_num+=1
    ws.write(row_num, 0, 'Дата формирования отчета', font_style)
    ws.write(row_num, 1,str(date.today()) , font_style)


    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    wb.save(response)
    return response


def rotate_img(path):
    try:
        image = Image.open(path)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        image.save(path)
        image.close()

    except (AttributeError, KeyError, IndexError):
        pass

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


def generate_pdf(list, contest_name, alias, reg_number):
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

    data = [[Paragraph(list[i][0], normal_style), Paragraph(list[i][1], normal_style)] for i in range(0, len(list))]

    table = Table(data, colWidths=[4 * cm, 14 * cm])

    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    c = canvas.Canvas(os.path.join(settings.MEDIA_ROOT, 'pdf', alias, f'{reg_number}.pdf'), pagesize=A4)
    c.setFont('Yandex', 20)
    c.drawString(20, 810, contest_name)
    c.drawImage(os.path.join(settings.BARCODE_MEDIA_ROOT, f'{reg_number}.png'), 340, 715)

    width2, height2 = table.wrapOn(c, width, height)
    table.drawOn(c, 1.2 * cm, A4[1] - height2 - 125, 0)
    c.save()


def send_mail_contest(secret, email, reg_number, message_template, name_contest, alias):
    list_emails = []
    list_emails.append(email)
    connection = get_connection(host=settings.EMAIL_CONTEST['host'],
                                port=settings.EMAIL_CONTEST['port'],
                                username=secret['user'],
                                password=secret['password'],
                                use_tls=settings.EMAIL_CONTEST['use_tls'])
    subject, from_email = name_contest, settings.EMAIL_CONTEST['from_contest']
    message = render_to_string(message_template, {'reg_number': reg_number})
    msg = EmailMultiAlternatives(subject, message, from_email, list_emails, connection=connection)
    msg.content_subtype = "html"
    try:
        if alias != 'teacher':
            attached_file = os.path.join(settings.MEDIA_ROOT, 'pdf', alias, f'{reg_number}.pdf')
        else:
            attached_file = os.path.join(settings.MEDIA_ROOT, 'zip', f'{reg_number}.zip')

        msg.attach_file(attached_file, mimetype='text/html')
        msg.send()
    except:
        msg.send()
    connection.close()


def send_mail_from_admin(secret, list_emails, message, subject):
    connection = get_connection(host=settings.EMAIL_CONTEST['host'],
                                port=settings.EMAIL_CONTEST['port'],
                                username=secret['user'],
                                password=secret['password'],
                                use_tls=settings.EMAIL_CONTEST['use_tls'])
    from_email = settings.EMAIL_CONTEST['from_contest']
    msg = EmailMultiAlternatives(subject, message, from_email, list_emails, connection=connection)
    msg.content_subtype = "html"
    msg.send()
    connection.close()


def generate_year():
    year_contest = '{}-{} год'.format(int(time.strftime("%Y", time.localtime()))-1,
                                      int(time.strftime("%Y", time.localtime())) + 1-1)
    return year_contest
