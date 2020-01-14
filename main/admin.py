from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

import csv
from main.tasks import send_mails_admin_tacks,nrusheva_tasks, artakiada_tasks, mymoskvici_tasks
from main.models import Artakiada,NRusheva,Mymoskvichi,Teacher
from main.forms import TextEditor

# Register your models here.


class BaseAdmin(admin.ModelAdmin):
    task_reg_info=None

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

    export_as_csv.short_description = 'Выгрузить список'


class ArtakiadaAdmin(BaseAdmin):
    task_reg_info=artakiada_tasks
    search_fields = ('reg_number','email','fio','fio_teacher')
    list_display = ('reg_number','status', 'fio',  'school', 'region','district','fio_teacher','teacher',)
    list_editable = ('status',)
    list_filter = ['status','district']
    actions=['send_emails','export_as_csv','send_reg_info']


class NRushevaAdmin(BaseAdmin):
    task_reg_info = nrusheva_tasks
    search_fields = ('reg_number', 'email', 'fio','fio_teacher')
    list_display = ('reg_number', 'status', 'fio', 'school', 'region', 'district', 'fio_teacher', 'teacher',)
    list_editable = ('status',)
    list_filter = ['status']
    actions = ['send_emails','export_as_csv','send_reg_info']


class MymoskvichiAdmin(BaseAdmin):
    task_reg_info = mymoskvici_tasks
    search_fields = ('reg_number', 'email', 'fio','fio_teacher')
    list_display = ('reg_number', 'status', 'fio_teacher', 'school', 'region', 'district', 'fio', 'teacher',)
    list_editable = ('status',)
    list_filter = ['status']
    actions = ['send_emails','export_as_csv','send_reg_info']


class TeacherAdmin(BaseAdmin):
    search_fields = ('email','fio',)
    list_display = ('fio', 'school', 'email','region', 'district','status',)
    list_filter = ['status']
    actions=['send_emails','export_as_csv']


admin.site.register(Artakiada, ArtakiadaAdmin)
admin.site.register(NRusheva,NRushevaAdmin)
admin.site.register(Mymoskvichi,MymoskvichiAdmin)
admin.site.register(Teacher,TeacherAdmin)