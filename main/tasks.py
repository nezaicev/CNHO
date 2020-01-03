from celery import shared_task
import secret
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







