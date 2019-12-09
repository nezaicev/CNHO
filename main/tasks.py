from celery import shared_task
import secret
from main import utils
from main.models import NRusheva, Artakiada, Mymoskvichi


@shared_task
def nrusheva_tasks(obj_id):
    obj = NRusheva.objects.get(id=obj_id)
    if obj:
        utils.generate_barcode(obj.reg_number)
        utils.generate_pdf(obj.get_parm_for_pdf(), obj.name, obj.reg_number)
        utils.send_mail_contest(secret.EMAIL_NRUSHEVA,obj.email,obj.reg_number,'test',obj.name)


@shared_task
def artakiada_tasks(obj_id):
    obj = Artakiada.objects.get(id=obj_id)
    if obj:
        utils.generate_barcode(obj.reg_number)
        utils.generate_pdf(obj.get_parm_for_pdf(), obj.name, obj.reg_number)
        utils.send_mail_contest(secret.EMAIL_ARTAKIADA, obj.email, obj.reg_number, 'test', obj.name)

@shared_task
def mymoskvici_tasks(obj_id):
    obj = Mymoskvichi.objects.get(id=obj_id)
    if obj:
        utils.send_mail_contest(secret.EMAIL_MYMOSKVICI, obj.email, obj.reg_number, 'test', obj.name)






