import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import Artakiada


class Command(BaseCommand):
    help = 'Сопоставление изображений по фамилиям'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        directory=kwargs["path"][0]
        files=os.listdir(directory)
        for f in files:
            fio=f.split()[0]

            user_list=Artakiada.objects.filter(fio__contains=fio).values()
            if user_list:
                for i in user_list:
                    print(f)
                    print(i['fio'],i['fio_teacher'],i['school'],i['reg_number'])
                    q=input("Введите y или n :")
                    if q=='y':
                        user=Artakiada.objects.get(reg_number=i['reg_number'])
                        user.image=os.path.join('images/artakiada',directory.split('/')[-1],f)
                        user.status='5'
                        user.save()
                        break
                    elif q=='n':
                        continue
