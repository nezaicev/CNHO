from django.contrib import admin
from main.models import Artakiada,NRusheva,Mymoskvichi

# Register your models here.

class ArtakiadaAdmin(admin.ModelAdmin):
    pass


class NRushevaAdmin(admin.ModelAdmin):
    pass


class MymoskvichiAdmin(admin.ModelAdmin):
    pass


admin.site.register(Artakiada, ArtakiadaAdmin)
admin.site.register(NRusheva,NRushevaAdmin)
admin.site.register(Mymoskvichi,MymoskvichiAdmin)