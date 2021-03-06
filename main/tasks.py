import os
import zipfile
from celery import shared_task
import secret
from django.conf import settings
from main import utils
from main.models import NRusheva, Artakiada, Mymoskvichi



@shared_task
def nrusheva_tasks(obj_id):
    message_template='letters/nrusheva_letters.html'
    obj = NRusheva.objects.get(id=obj_id)
    if obj:
        utils.generate_barcode(obj.reg_number)
        utils.generate_pdf(obj.get_parm_for_pdf(), obj.name,obj.alias, obj.reg_number)
        utils.send_mail_contest(secret.EMAIL_NRUSHEVA,obj.email,obj.reg_number,message_template,obj.name,obj.alias)
        utils.rotate_img(obj.image.path)


@shared_task
def artakiada_tasks(obj_id):
    message_template='letters/artakiada_letters.html'
    obj = Artakiada.objects.get(id=obj_id)
    if obj:
        utils.generate_barcode(obj.reg_number)
        utils.generate_pdf(obj.get_parm_for_pdf(), obj.name,obj.alias, obj.reg_number)
        utils.send_mail_contest(secret.EMAIL_ARTAKIADA, obj.email, obj.reg_number, message_template, obj.name,obj.alias)


@shared_task
def mymoskvici_tasks(obj_id):
    message_template='letters/mymoskvichi_letters.html'
    obj = Mymoskvichi.objects.get(id=obj_id)
    if obj:
        utils.generate_barcode(obj.reg_number)
        utils.generate_pdf(obj.get_parm_for_pdf(), obj.name, obj.alias, obj.reg_number)
        utils.send_mail_contest(secret.EMAIL_MYMOSKVICI, obj.email, obj.reg_number, message_template, obj.name,obj.alias)


@shared_task
def send_mails_admin_tacks(list_email,message,subject):
    utils.send_mail_from_admin(secret.EMAIL_ALL,list_email,message,subject)


@shared_task
def send_mails_to_teacher_with_zip(teacher_id,field_names,exclude_field,email,message_template,filter):
    if filter['artakiada']=='art_level_2':
        data_xls = Artakiada.objects.filter(teacher_id=teacher_id, status__in=[2,3, 4])
        data=data_xls.filter(status__in=[3,4])
    else:
        data = Artakiada.objects.filter(teacher_id=teacher_id)
    xls_path = os.path.join(settings.MEDIA_ROOT, 'xls', '{}.xls'.format(teacher_id))
    utils.generate_xls(data_xls, field_names, exclude_field, xls_path)
    with zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, 'zip', '{}.zip'.format(str(teacher_id))), 'w') as z:
        z.write(xls_path, '{}.xls'.format(teacher_id))
        for obj in data:
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdf', Artakiada.alias, f'{obj.reg_number}.pdf')
            if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
                z.write(pdf_path, f'{obj.reg_number}.pdf')
            else:
                utils.generate_barcode(obj.reg_number)
                utils.generate_pdf(obj.get_parm_for_pdf(), obj.name, obj.alias, obj.reg_number)
                z.write(pdf_path, f'{obj.reg_number}.pdf')
    utils.send_mail_contest(secret.EMAIL_ALL,email,teacher_id,message_template,Artakiada.name,alias='teacher')







