from django.contrib import admin
from main.models import Artakiada,NRusheva,Mymoskvichi

# Register your models here.

class ArtakiadaAdmin(admin.ModelAdmin):
    search_fields = ('reg_number','email','fio','fio_teacher')
    list_display = ('reg_number','status', 'fio',  'school', 'region','district','fio_teacher','teacher',)
    list_editable = ('status',)


class NRushevaAdmin(admin.ModelAdmin):
    search_fields = ('reg_number', 'email', 'fio')



class MymoskvichiAdmin(admin.ModelAdmin):
    search_fields = ('reg_number', 'email', 'fio')


admin.site.register(Artakiada, ArtakiadaAdmin)
admin.site.register(NRusheva,NRushevaAdmin)
admin.site.register(Mymoskvichi,MymoskvichiAdmin)