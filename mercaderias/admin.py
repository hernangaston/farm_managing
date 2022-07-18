#! /usr/bin/env python3

from django.contrib import admin

from .models import *
# Register your models here.

@admin.register(Destino)
class CompradorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'cuit')
    ordering = ('nombre',)
    list_editable = ('nombre', 'cuit')

@admin.register(Destinatario)
class CompradorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'cuit')
    ordering = ('nombre',)
    list_editable = ('nombre', 'cuit')

@admin.register(CartaDePorte)
class CartaDePorte(admin.ModelAdmin):
    list_display = ['numero', 'cosecha', 'titular', 'grano', 'peso_neto']
    list_filter = ('cosecha', 'grano')
    search_fields = ('numero',)
    ordering = ('updated_at',)

@admin.register(CartaDePorteDescargada)
class CartaDePorteDescargadaAdmin(admin.ModelAdmin): 
    list_filter = ('cp__cosecha', 'cp__grano')
    list_display = ['cp', 'contrato', 'kilos_descargados', 'cosecha_display_admin']
    search_fields = ['cp__cosecha', 'cp__numero']
    ordering = ('updated_at',)

@admin.register(ContratoMercaderia)
class ContratoMercaderiaAdmin(admin.ModelAdmin):
    list_display = ['nro_comprador', 'producto', 'kilos_pactados']
    ordering = ('updated_at',)

@admin.register(Campo)
class CampoAdmin(admin.ModelAdmin):
   
    ordering = ('updated_at',)

@admin.register(PlanSiembra)
class PlanSiembraAdmin(admin.ModelAdmin):
    list_display = ['campo', 'cultivo', 'superficie_sembrada', 'campania']
    list_filter = ('cultivo', 'campania')
    ordering = ('updated_at',)

@admin.register(OrdenDeLabor)
class OrdenDeLaborAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'labor', 'cultivo', 'contratista']
    ordering = ('updated_at',)
    list_editable = ('contratista',)


@admin.register(ItemLabor)
class ItemLaborAdmin(admin.ModelAdmin):
    list_display = ['insumo', 'dosis', 'orden']
    ordering = ('updated_at',)
    list_editable = ('dosis',)

@admin.register(Arrendamiento)
class ContratoArrendamientoAdmin(admin.ModelAdmin):
    list_display = ['arrendador']
    ordering = ('updated_at',)
    #list_editable = ('dosis',)

