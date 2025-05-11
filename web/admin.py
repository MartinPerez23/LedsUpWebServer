from django.contrib import admin

from .models import TipoProducto, Producto, ImagenesProducto, CaracteristicasProducto, VideosProducto, ImagenesGaleria, \
    Galeria


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


class ImagenesGaleriaEnLinea(admin.TabularInline):
    verbose_name_plural = 'Imagenes de la Galeria'
    verbose_name = 'Imagen de la Galeria'
    model = ImagenesGaleria
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


class GaleriaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre']}),
        (None, {'fields': ['fecha']}),
        (None, {'fields': ['detalle']}),
    ]
    inlines = [ImagenesGaleriaEnLinea]

    list_filter = ['fecha']
    search_fields = ['nombre']
    list_display = ('nombre', 'fecha', 'detalle')


admin.site.register(Galeria, GaleriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(TipoProducto)
