from django.contrib import admin
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseNotFound,FileResponse

import csv
import os
import xlwt
from main.tasks import send_mails_admin_tacks,nrusheva_tasks, artakiada_tasks, mymoskvici_tasks
from main.models import Artakiada,NRusheva,Mymoskvichi,Teacher
from main.forms import TextEditor
from main.utils import generate_report

# Register your models here.


class BaseAdmin(admin.ModelAdmin):
    name=None
    task_reg_info=None

    def export_list_info(self,request,queryset):
        meta = self.model._meta
        reg_number=queryset[0].reg_number
        file_location=None
        try:
            file_location = os.path.join(settings.MEDIA_ROOT, 'pdf', self.name, f'{reg_number}.pdf')
            response = FileResponse(open(file_location, 'rb'))
            return response
        except:
            self.message_user(request, "{} не найден".format(file_location))
            return HttpResponseRedirect(request.get_full_path())

    export_list_info.short_description='Скачать регистрационный лист участника'

    def send_reg_info(self,request,queryset):
        for obj in queryset:
            self.task_reg_info.delay(obj.id)
        self.message_user(request, "{} отправлено".format(queryset.count()))
        return HttpResponseRedirect(request.get_full_path())
    send_reg_info.short_description = 'Отправить регистрационные данные'

    def send_emails(self,request,queryset):
        if 'apply' in request.POST:
            list_emails=list(queryset.values_list('email',flat=True))
            send_mails_admin_tacks.delay(list_emails , request.POST['editor'], request.POST['theme'])
            self.message_user(request, "{} отправлено".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())

        return render(request, 'admin/editor_emails.html', context={'orders': queryset, 'form': TextEditor()})

    send_emails.short_description = 'Отправить письмо'


    def export_as_xls(self,request,queryset):
        exclude_field=['date_reg','teacher','image']
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename={}.xls'.format(meta)

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
            ridx+=1
            for cidx, field in enumerate(obj._meta.fields):
                if field.name not in exclude_field:
                    if field.choices:
                        val = obj._get_FIELD_display(field)
                        ws.write(ridx, cidx, val, font_style)
                    else:
                        val = getattr(obj, field.name)
                        ws.write(ridx, cidx, val, font_style)

        wb.save(response)
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
            row=[]
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
    task_reg_info=artakiada_tasks
    search_fields = ('reg_number','email','fio','fio_teacher')
    list_display = ('reg_number', 'fio',  'school', 'region','district','fio_teacher','teacher','status')
    list_editable = ('status',)
    list_filter = ['status','district']
    actions=['send_emails','export_as_csv','send_reg_info','export_list_info','export_as_xls','get_report']

    def get_report(self,request,queryset):
        response= generate_report(Artakiada)
        return response
    get_report.short_description = 'Сформировать отчет'



class NRushevaAdmin(BaseAdmin):
    name = 'nrusheva'
    task_reg_info = nrusheva_tasks
    search_fields = ('reg_number', 'email', 'fio','fio_teacher')
    list_display = ('reg_number','status','image_tag', 'fio', 'school', 'region', 'district', 'fio_teacher', 'teacher',)
    list_editable = ('status',)
    list_filter = ['status']
    actions = ['send_emails','export_as_csv','send_reg_info','export_list_info','export_as_xls']


class MymoskvichiAdmin(BaseAdmin):
    name='mymoskvichi'
    task_reg_info = mymoskvici_tasks
    search_fields = ('reg_number', 'email', 'fio','fio_teacher')
    list_display = ('reg_number', 'fio_teacher', 'school', 'region', 'district', 'fio', 'teacher', 'status')
    list_editable = ('status',)
    list_filter = ['status']
    actions = ['send_emails','export_as_csv','send_reg_info','export_list_info','export_as_xls',]


class TeacherAdmin(BaseAdmin):
    search_fields = ('email','fio',)
    list_display = ('fio', 'school', 'email','region', 'district','status',)
    list_filter = ['status']
    actions=['send_emails','export_as_csv','export_as_xls']


admin.site.register(Artakiada, ArtakiadaAdmin)
admin.site.register(NRusheva,NRushevaAdmin)
admin.site.register(Mymoskvichi,MymoskvichiAdmin)
admin.site.register(Teacher,TeacherAdmin)