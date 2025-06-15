from django.contrib import admin

from .models import (
    TipoProducto, Producto, ImagenesProducto, CaracteristicasProducto,
    VideosProducto, ImagenesEventos, Evento, Errores
)


class VideosProductoEnLinea(admin.TabularInline):
    verbose_name_plural = 'Videos del Producto'
    verbose_name = 'Video del Producto'
    model = VideosProducto
    extra = 1


class ImagenesProductoEnLinea(admin.TabularInline):
    verbose_name_plural = 'Imagenes del Producto'
    verbose_name = 'Imagen del Producto'
    model = ImagenesProducto
    extra = 1


class ImagenesEventosEnLinea(admin.TabularInline):
    verbose_name_plural = 'Imagenes de Eventos'
    verbose_name = 'Imagen del Evento'
    model = ImagenesEventos
    extra = 1


class CaracteristicasProductoEnLinea(admin.TabularInline):
    verbose_name_plural = 'Caracteristicas del Producto'
    verbose_name = 'Caracteristica del Producto'
    model = CaracteristicasProducto
    extra = 1


class ProductoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre_producto']}),
        (None, {'fields': ['tipo_producto']}),
        (None, {'fields': ['detalles']}),
        (None, {'fields': ['precio']}),
    ]
    inlines = [CaracteristicasProductoEnLinea, ImagenesProductoEnLinea, VideosProductoEnLinea]

    list_filter = ['fecha_creacion']
    search_fields = ['nombre_producto']
    list_display = ('nombre_producto', 'fecha_creacion', 'creado_recientemente')


class EventoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre_evento']}),
        (None, {'fields': ['fecha_de_evento']}),
        (None, {'fields': ['pie_de_imagen']}),
    ]
    inlines = [ImagenesEventosEnLinea]

    list_filter = ['fecha_de_evento']
    search_fields = ['nombre_evento']
    list_display = ('nombre_evento', 'fecha_de_evento', 'pie_de_imagen')


class ErroresAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['usuario', 'origen', 'detalle', 'contexto']}),
        ('Seguimiento', {'fields': ['estado', 'asignado_a', 'comentarios']}),
    ]

    list_display = ('id', 'fecha_creacion', 'usuario', 'origen', 'estado', 'asignado_a')
    list_filter = ['estado', 'origen', 'fecha_creacion']
    search_fields = ['detalle', 'contexto', 'usuario__username']


admin.site.register(Evento, EventoAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(TipoProducto)
admin.site.register(Errores, ErroresAdmin)
