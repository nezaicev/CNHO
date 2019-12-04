from celery import shared_task
from main import utils
from main.models import NRusheva


@shared_task
def generate_pdf(obj_id):
    obj = NRusheva.objects.get(id=obj_id)
    utils.generate_barcode(obj.reg_number)
    utils.generate_pdf(obj.get_parm_for_pdf(), obj.name, obj.reg_number)
