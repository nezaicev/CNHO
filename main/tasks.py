from celery import shared_task
from main import utils
from main.models import NRusheva


@shared_task
def generate_pdf(obj_id):
    obj = NRusheva.objects.get(id=obj_id)
    utils.generate_barcode(obj.reg_number)
    utils.generate_pdf(obj.get_parm_for_pdf(), obj.name, obj.reg_number)



def send_mail_contest(secret, reg_number, name_contest, email, message):
    connection = get_connection(host=settings.EMAIL_CONTEST['host'],
                                port=settings.EMAIL_CONTEST['port'],
                                username=secret['user'],
                                password=secret['password'],
                                use_tls=settings.EMAIL_CONTEST['use_tls'])

    subject, from_email = 'tema', secret['user']
    msg = EmailMultiAlternatives(subject,subject, from_email, email, connection=connection)
    msg.content_subtype = "html"
    attached_file = os.path.join(settings.MEDIA_ROOT, 'pdf', f'{reg_number}.pdf')
    msg.attach_file(attached_file,mimetype='text/html')

    connection.close()


