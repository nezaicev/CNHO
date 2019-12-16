from django.contrib import admin
from main.models import Artakiada,NRusheva,Mymoskvichi,Teacher

# Register your models here.


class ArtakiadaAdmin(admin.ModelAdmin):
    search_fields = ('reg_number','email','fio','fio_teacher')
    list_display = ('reg_number','status', 'fio',  'school', 'region','district','fio_teacher','teacher',)
    list_editable = ('status',)


class NRushevaAdmin(admin.ModelAdmin):
    search_fields = ('reg_number', 'email', 'fio')


class MymoskvichiAdmin(admin.ModelAdmin):
    search_fields = ('reg_number', 'email', 'fio')


class TeacherAdmin(admin.ModelAdmin):
    search_fields = ('email','fio',)
    list_display = ('fio', 'school', 'email','region', 'district','status',)


admin.site.register(Artakiada, ArtakiadaAdmin)
admin.site.register(NRusheva,NRushevaAdmin)
admin.site.register(Mymoskvichi,MymoskvichiAdmin)
admin.site.register(Teacher,TeacherAdmin)