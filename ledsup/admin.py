# Register your models here.
from django.contrib import admin

from .models import Dispositivo, Showroom, OrdenDispositivosEnShowroom


class OrdenDispositivosEnShowroomInline(admin.TabularInline):
    model = OrdenDispositivosEnShowroom
    extra = 1


class DispositivoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['usuario']}),
        (None, {'fields': ['nombre_dispositivo']}),
        (None, {'fields': ['numero_ip']}),
        (None, {'fields': ['universo']}),
        (None, {'fields': ['tamano_paquetes']}),
        (None, {'fields': ['matriz_x']}),
        (None, {'fields': ['matriz_y']}),
        (None, {'fields': ['patch']}),
        (None, {'fields': ['tipo_led']}),
    ]


class ShowroomAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['usuario']}),
        (None, {'fields': ['nombre_showroom']}),
    ]
    inlines = (OrdenDispositivosEnShowroomInline,)


admin.site.register(Dispositivo, DispositivoAdmin)
admin.site.register(Showroom, ShowroomAdmin)

