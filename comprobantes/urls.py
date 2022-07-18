#! /usr/bin/env python3
from django.views.generic import TemplateView, View
from django.urls import path
from .views import *

app_name = 'fyp'

urlpatterns = [
    path('', index, name='index'),
    path('list_empresa/', EmpresaList.as_view(), name='list-empresa'),
    path('empresa/', EmpresaCreate.as_view(), name='create-empresa'),
    path('<int:pk>/change_empresa/', changeEmpresa, name='change-empresa'),
    #---------------------------------- URLS PAGOS ----------------------------------
    path('list_pagos/', PagoListView.as_view(), name='list-pagos'),
    path('add_pagos/', PagoCreateView.as_view(), name='add-pagos'),
    path('<int:pk>/detail_pago/', PagoDetailView.as_view(), name='detail-pago'),
    path('<int:pk>/delete_pago/', PagoDeleteView.as_view(), name='delete-pago'),
    path('<int:pk>/update_pago/', PagoUpdateView.as_view(), name='update-pago'),
    path('ajax/load-datas/', load_datas, name='ajax_load_datas'), # AJAX
    #---------------------------------- URLS FACTURAS ----------------------------------
    path('list_facturas/', FacturasListView.as_view(), name='list-facturas'),
    path('add_facturas/', FacturaCreateView.as_view(), name='add-facturas'),
    path('<int:pk>/detail_factura/', FacturaDetailView.as_view(), name='detail-factura'),
    path('<int:pk>/delete_factura/', FacturaDeleteView.as_view(), name='delete-factura'),
    path('<int:pk>/update_factura/', FacturaUpdateView.as_view(), name='update-factura'),
    #----------------------------------NOTAS---------------------------------------------------
    path('add_nc/', NotasCreditoCreateView.as_view(), name='add-nota-de-credito'),
    path('add_nd/', NotasDebitoCreateView.as_view(), name='add-nota-de-debito'),
    #---------------------------------- URLS PROVEEDORES ----------------------------------
    path('list_proveedores/', ListProveedorView.as_view(), name='list-proveedores'),
    path('add_proveedor/', ProveedorCreateView.as_view(), name='add-proveedor'),
    path('<int:pk>/detail_proveedor/', ProveedorDetailView.as_view(), name='detail-proveedor'),
    path('<int:pk>/delete_proveedor/', ProveedorDeleteView.as_view(), name='delete-proveedor'),
    path('<int:pk>/update_proveedor/', ProveedorUpdateView.as_view(), name='update-proveedor'),
    #---------------------------------- URLS INSTRUMENTO PAGO ----------------------------------
    path('add_instrumento/', AddInstrumento.as_view(), name='add-instrumento'),
    path('list_instrumento/', ListIntrumento.as_view(), name='list-instrumentos'),
    #---------------------------------- URLS ARTICULO -------------------------------------------
    path('list_articulo/', ArticuloListView.as_view(), name='list-articulos'),
    path('add_articulo/', ArticuloCreate.as_view(), name='add-articulo'),
    path('<int:pk>/detail_articulo/', ArticuloDetailView.as_view(), name='detail-articulo'),
    path('<int:pk>/update_articulo/', ArticuloUpdateView.as_view(), name='update-articulo'),
    path('<int:pk>/delete_articulo/', ArticuloDeleteView.as_view(), name='delete-articulo'),
    #---------------------------------- URLS ITEM FACTURA ----------------------------------
    path('<int:pk>/delete_item/', ItemFacturaDeleteView.as_view(), name='delete-itemfactura'),
    #---------------------------------- URLS CUENTAS CORRIENTES ----------------------------------
    path('cuenta_corriente/', CuentaCorrienteView.as_view(), name='cuenta-corriente-proveedor'),
    #---------------------------------- REPORTE COMPROBANTES ----------------------------------
    path('reporte_comprobantes/', ReporteComprobantes.as_view(), name='reporte-comprobantes'),
    path('reporte_costos/', ReporteCostos.as_view(), name='reporte-costos'),
]
