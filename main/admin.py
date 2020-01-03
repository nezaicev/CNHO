from django.contrib import admin
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives, get_connection
import secret
from main.tasks import send_mails_admin_tacks
from main.models import Artakiada,NRusheva,Mymoskvichi,Teacher
from main.forms import TextEditor,MymoskviciContestForm,EmailForm

# Register your models here.


class BaseAdmin(admin.ModelAdmin):
    def send_emails(self,request,queryset):
        if 'apply' in request.POST:
            list_emails=list(queryset.values_list('email',flat=True))
            send_mails_admin_tacks.delay(list_emails , request.POST['editor'], request.POST['theme'])
            self.message_user(request, "{} отправлено".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())

        return render(request, 'admin/editor_emails.html', context={'orders': queryset, 'form': TextEditor()})

    send_emails.short_description = 'Отправить письмо'


class ArtakiadaAdmin(BaseAdmin):
    search_fields = ('reg_number','email','fio','fio_teacher')
    list_display = ('reg_number','status', 'fio',  'school', 'region','district','fio_teacher','teacher',)
    list_editable = ('status',)
    actions=['send_emails']


class NRushevaAdmin(BaseAdmin):
    search_fields = ('reg_number', 'email', 'fio','fio_teacher')
    list_display = ('reg_number', 'status', 'fio', 'school', 'region', 'district', 'fio_teacher', 'teacher',)
    list_editable = ('status',)
    actions = ['send_emails']


class MymoskvichiAdmin(BaseAdmin):
    search_fields = ('reg_number', 'email', 'fio','fio_teacher')
    list_display = ('reg_number', 'status', 'fio_teacher', 'school', 'region', 'district', 'fio', 'teacher',)
    list_editable = ('status',)
    actions = ['send_emails']


class TeacherAdmin(BaseAdmin):
    search_fields = ('email','fio',)
    list_display = ('fio', 'school', 'email','region', 'district','status',)
    actions=['send_emails']


admin.site.register(Artakiada, ArtakiadaAdmin)
admin.site.register(NRusheva,NRushevaAdmin)
admin.site.register(Mymoskvichi,MymoskvichiAdmin)
admin.site.register(Teacher,TeacherAdmin)