from django.contrib import admin
from main.models import Artakiada,NRusheva,Mymoskvichi

# Register your models here.

class ArtakiadaAdmin(admin.ModelAdmin):
    search_fields = ('reg_number','email','fio')
    list_display = ('reg_number', 'fio', 'school', 'teacher','status')
    list_editable = ('status',)


class NRushevaAdmin(admin.ModelAdmin):
    search_fields = ('reg_number', 'email', 'fio')



class MymoskvichiAdmin(admin.ModelAdmin):
    search_fields = ('reg_number', 'email', 'fio')


admin.site.register(Artakiada, ArtakiadaAdmin)
admin.site.register(NRusheva,NRushevaAdmin)
admin.site.register(Mymoskvichi,MymoskvichiAdmin)