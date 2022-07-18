#! /usr/bin/env python3
from django.contrib import admin

# Register your models here.

from .models import Factura, Articulo, Proveedor, Pagos, InstrumentoPago, ItemFactura, NotaDeCredito, NotaDeDebito
from .forms import *



@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'numero', 'total', 'fecha_vto', 'rubro','estado_pago', 'cosecha', 'titular')
    ordering = ('fecha',)
    search_fields = ['proveedor__nombre']
    list_filter = ('estado_pago', 'proveedor', 'rubro')
    list_editable = ('estado_pago', 'rubro', 'cosecha', 'titular')

@admin.register(NotaDeCredito)
class NcAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'numero', 'proveedor','total', 'fecha_vto', 'rubro','estado_pago')
    ordering = ('fecha',)
    list_filter = ('estado_pago', 'proveedor', 'rubro')
    list_editable = ('estado_pago', 'rubro')

@admin.register(NotaDeDebito)
class NdAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'numero', 'total', 'fecha_vto', 'rubro','estado_pago')
    ordering = ('fecha',)
    list_filter = ('estado_pago', 'proveedor', 'rubro')
    list_editable = ('estado_pago', 'rubro')


@admin.register(Pagos)
class PagosAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha','proveedor', 'importe_instrumentos', 'importe_facturas')
    list_filter = ('proveedor',)
    search_fields = ['proveedor__nombre']
    ordering = ('fecha',)
    form = PagoForm
    

@admin.register(InstrumentoPago)
class InstrumentoPagoAdmin(admin.ModelAdmin):
    ordering = ('fecha',)   
    list_display = ('instrumento', 'proveedor', 'estado_uilizado',)
    search_fields = ['proveedor__nombre']
    list_editable = ('estado_uilizado',)

@admin.register(ItemFactura)
class ItemFacturaAdmin(admin.ModelAdmin):
    ordering = ('articulo',)   
    list_display = ('factura','articulo', 'cantidad', 'precio_unitario',)
    list_editable = ('articulo',)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre','cuit')
    search_fields = ('cuit',)
    
admin.site.register(Articulo)