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
        utils.generate_pdf(obj.get_parm_for_pdf(), obj.name, obj.reg_number)
        utils.send_mail_contest(secret.EMAIL_NRUSHEVA,obj.email,obj.reg_number,message_template,obj.name)


@shared_task
def artakiada_tasks(obj_id):
    message_template='letters/artakiada_letters.html'
    obj = Artakiada.objects.get(id=obj_id)
    if obj:
        utils.generate_barcode(obj.reg_number)
        utils.generate_pdf(obj.get_parm_for_pdf(), obj.name, obj.reg_number)
        utils.send_mail_contest(secret.EMAIL_ARTAKIADA, obj.email, obj.reg_number, message_template, obj.name)


@shared_task
def mymoskvici_tasks(obj_id):
    message_template='letters/mymoskvichi_letters.html'
    obj = Mymoskvichi.objects.get(id=obj_id)
    if obj:
        utils.send_mail_contest(secret.EMAIL_MYMOSKVICI, obj.email, obj.reg_number, message_template, obj.name)






