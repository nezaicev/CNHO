import os
import csv
import xlwt
import zipfile
import time

from django.contrib import admin
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.utils.translation import gettext_lazy as _
import secret
from main.tasks import send_mails_admin_tacks, nrusheva_tasks, artakiada_tasks, mymoskvici_tasks, send_mails_to_teacher_with_zip
from main.models import Artakiada, NRusheva, Mymoskvichi, Teacher
from main.forms import TextEditor
from main.utils import generate_report, generate_pdf,generate_barcode,generate_xls,send_mail_contest


# Register your models here.


class ContestListFilter(admin.SimpleListFilter):
    title = ('Конкурсы')
    parameter_name = 'artakiada'

    def lookups(self, request, model_admin):
        return (
            ('art_all', ('Артакиада')),
            ('art_level_2', ('Победители и призеры 2 тур (Артакиада) ')),
            ('mosk_all', ('Мы Москвичи')),
            ('nrush_all', ('Н.Рушева')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'art_all':
            return queryset.filter(id__in=Artakiada.objects.values('teacher_id'))
        if self.value() == 'art_level_2':
            return queryset.filter(id__in=Artakiada.objects.filter(status__in=[3,4]).values('teacher_id'))

        if self.value() == 'mosk_all':
            return queryset.filter(id__in=Mymoskvichi.objects.values('teacher_id'))
        if self.value() == 'nrush_all':
            return queryset.filter(id__in=NRusheva.objects.values('teacher_id'))


class BaseAdmin(admin.ModelAdmin):
    name = None
    task_reg_info = None

    def export_list_info(self, request, queryset):
        meta = self.model._meta
        reg_number = queryset[0].reg_number
        file_location = None
        try:
            file_location = os.path.join(settings.MEDIA_ROOT, 'pdf', self.name, f'{reg_number}.pdf')
            response = FileResponse(open(file_location, 'rb'))
            return response
        except:
            self.message_user(request, "{} не найден".format(file_location))
            return HttpResponseRedirect(request.get_full_path())

    export_list_info.short_description = 'Скачать регистрационный лист участника'

    def send_reg_info(self, request, queryset):
        for obj in queryset:
            self.task_reg_info.delay(obj.id)
        self.message_user(request, "{} отправлено".format(queryset.count()))
        return HttpResponseRedirect(request.get_full_path())

    send_reg_info.short_description = 'Отправить регистрационные данные'

    def send_emails(self, request, queryset):
        if 'apply' in request.POST:
            list_emails = list(queryset.values_list('email', flat=True))
            send_mails_admin_tacks.delay(list_emails, request.POST['editor'], request.POST['theme'])
            self.message_user(request, "{} отправлено".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())

        return render(request, 'admin/editor_emails.html', context={'orders': queryset, 'form': TextEditor()})

    send_emails.short_description = 'Отправить письмо'

    def export_as_xls(self, request, queryset):
        exclude_field = ['date_reg', 'teacher', 'image']
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        path = os.path.join(settings.MEDIA_ROOT, 'xls', 'report.xls')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename={}.xls'.format(meta)
        generate_xls(queryset,field_names,exclude_field,path)
        response=FileResponse(open(path, 'rb'))
        return response

    export_as_xls.short_description = 'Выгрузить список Excel'

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)

        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response, delimiter=',')

        writer.writerow(field_names)
        for obj in queryset:
            row = []
            for field in obj._meta.fields:
                if field.choices:
                    val = obj._get_FIELD_display(field)
                    row.append(val)
                else:
                    val = getattr(obj, field.name)
                    row.append(val)
            writer.writerow(row)
        return response

    export_as_csv.short_description = 'Выгрузить список СSV'


class ArtakiadaAdmin(BaseAdmin):
    name = 'artakiada'
    task_reg_info = artakiada_tasks
    search_fields = ('reg_number', 'email', 'fio', 'fio_teacher')
    list_display = ('reg_number', 'fio', 'school', 'region', 'district', 'fio_teacher', 'teacher', 'status')
    list_editable = ('status',)
    list_filter = ['status', 'district']
    actions = ['send_emails', 'export_as_csv', 'send_reg_info', 'export_list_info', 'export_as_xls', 'get_report']

    def get_report(self, request, queryset):
        response = generate_report(Artakiada)
        return response

    get_report.short_description = 'Сформировать отчет'


class NRushevaAdmin(BaseAdmin):
    name = 'nrusheva'
    task_reg_info = nrusheva_tasks
    search_fields = ('reg_number', 'email', 'fio', 'fio_teacher')
    list_display = (
        'reg_number', 'status', 'image_tag', 'fio', 'school', 'region', 'district', 'fio_teacher', 'teacher',)
    list_editable = ('status',)
    list_filter = ['status']
    actions = ['send_emails', 'export_as_csv', 'send_reg_info', 'export_list_info', 'export_as_xls']


class MymoskvichiAdmin(BaseAdmin):
    name = 'mymoskvichi'
    task_reg_info = mymoskvici_tasks
    search_fields = ('reg_number', 'email', 'fio', 'fio_teacher')
    list_display = ('reg_number', 'fio_teacher', 'school', 'region', 'district', 'fio', 'teacher', 'status')
    list_editable = ('status',)
    list_filter = ['status']
    actions = ['send_emails', 'export_as_csv', 'send_reg_info', 'export_list_info', 'export_as_xls', ]


class TeacherAdmin(BaseAdmin):
    search_fields = ('email', 'fio',)
    list_display = ('fio', 'school', 'email', 'region', 'district', 'status',)
    list_filter = ('status', ContestListFilter,'region')
    actions = ['send_emails', 'export_as_csv', 'export_as_xls','send_zip_with_pdf_artakiada']

    def send_zip_with_pdf_artakiada(self,request,queryset):
        meta = Artakiada._meta
        exclude_field = ['date_reg', 'teacher', 'image']
        field_names = [field.name for field in meta.fields]
        message_template='letters/artakiada_2_level_leter.html'
        filter=request.GET
        for i in queryset:
            send_mails_to_teacher_with_zip.delay(i.id,field_names,exclude_field,i.email,message_template,filter)
    send_zip_with_pdf_artakiada.short_description = 'Рассылка списков и рег. листов (артакиада)'


admin.site.register(Artakiada, ArtakiadaAdmin)
admin.site.register(NRusheva, NRushevaAdmin)
admin.site.register(Mymoskvichi, MymoskvichiAdmin)
admin.site.register(Teacher, TeacherAdmin)
