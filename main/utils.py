import re
import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
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


def send_mail_contest(secret, email,reg_number,message_template,name_contest):
    list_emails=[]
    list_emails.append(email)
    connection = get_connection(host=settings.EMAIL_CONTEST['host'],
                                port=settings.EMAIL_CONTEST['port'],
                                username=secret['user'],
                                password=secret['password'],
                                use_tls=settings.EMAIL_CONTEST['use_tls'])
    subject, from_email = name_contest, secret['user']
    message=render_to_string(message_template,{'reg_number':reg_number})
    msg = EmailMultiAlternatives(subject,message, from_email, list_emails, connection=connection)
    msg.content_subtype = "html"
    try:
        attached_file = os.path.join(settings.MEDIA_ROOT, 'pdf', f'{reg_number}.pdf')
        msg.attach_file(attached_file, mimetype='text/html')
        msg.send()
    except:
        msg.send()
    connection.close()



