#! /usr/bin/env python3
from django.urls import path, re_path
from .views import *


app_name = 'mer'

urlpatterns = [
    path('lista_cp/', ListaCp.as_view(), name='lista-cp'),
    path('crear_cp/', CartaDePorteCreate.as_view(), name='crear-cp'),
    path('<int:pk>/delete_cp/', DeleteCP.as_view(), name='delete-cp'),
    path('aplica_cp/', Aplicaciones.as_view(), name='aplica-cp'),
    path('lista_descargas_cp/', AplicacionesList.as_view(), name='lista-descargas-cp'),
    path('<int:pk>/editar_aplicacion_cp/', AplicacionesUpdateView.as_view(), name='editar-aplicacion-cp'),
    path('<int:pk>/delete_aplicacion_cp/', DeleteAplicacion.as_view(), name='delete-aplicacion-cp'),
    path('contratos_cp/', Contratos.as_view(), name='contratos-cp'),
    path('list_contratos_cp/', ContratosList.as_view(), name='list-contratos-cp'),
    path('<int:pk>/delete_contrato_cp/', ContratoDelete.as_view(), name='delete-contrato-cp'),
    path('<int:pk>/ver_contrato_cp/', ContratoDetail.as_view(), name='detalle-contrato-cp'),
    #--------FIJACIONES--------------------
    path('crear_fijacion/', CrearFijacion.as_view(), name='crear-fijacion'),
    path('crear_pesificacion/', CrearPesificacion.as_view(), name='crear-pesificacion'),
    #------------REPORTES--------------------------------
    path('reportes/', Reportes.as_view(), name='reportes'),
    path('planes/', PlanSiembraListView.as_view(), name='planes'),
    path('existencias/', CuentaMercaderia.as_view(), name='existencias'),
    #------------LABORES--------------------------------
    path('crear_labor/', OrdenDeLaborCreate.as_view(), name='crear-labor'),
    path('listar_labor/', OrdenDeLaborList.as_view(), name='listar-labor'),
    path('<int:pk>/eliminar_labor/', OrdenDeLaborDelete.as_view(), name='delete-labor'),
    #------------LABORES--------------------------------
    path('listar_stock/', listadoStock, name='listar-stock'),
    #------------LOTES--------------------------------
    path('listar_lotes/', ListaLotes.as_view(), name='listar-lotes'),
    path('crear_lote/', CreateLote.as_view(), name='crear-lote'),
    #------------ARRENDAMIENTOS--------------------------------
    path('crear_arrendamiento/', CrearArrendamiento.as_view(), name='crear-arrendamiento'),
    path('listar_arrendamiento/', ListaArrendamiento.as_view(), name='listar-arrendamientos'),
    path('<int:pk>/eliminar_arrendamiento/', EliminarArrendamiento.as_view(), name='eliminar-arrendamiento')

]
