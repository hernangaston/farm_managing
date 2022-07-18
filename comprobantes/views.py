#! /usr/bin/env python3
import json
import datetime
import requests

from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.core.serializers import serialize
from django.template import loader

from django.shortcuts import get_object_or_404, get_list_or_404

from .models import *
from .forms import PagoForm, ProveedorForm, InstrumentoPagoForm, FacturaForm,\
     ArticuloForm, ItemsFormset, EmpresaForm 
'''NcForm, NdForm,'''

from django.contrib.auth.models import User

from mercaderias.models import CartaDePorteDescargada



#------------- INICIAL ------------
def get_tipo_moneda(url):
    try:
        response = requests.get(url, params={})
        if response.status_code == 200:
            return response.json()
    except:
        pass


def sendnavbar(request):
    context = {}
    return render(request,'navigation.html', context)
   

def index(request):
    message = 'This is gestion index with render. TEST'  

    api_url = 'https://api-dolar-argentina.herokuapp.com/'
    dolar_oficial_url=api_url+'api/dolaroficial'
    dolar_blue_url=api_url+'api/dolarblue'
    dolar=''
    try:
        dolar = get_tipo_moneda(dolar_oficial_url)
        dolar_blue = get_tipo_moneda(dolar_blue_url)
        request.session['dolar_compra'] = dolar['compra']
        request.session['dolar_venta'] = dolar['venta']
        request.session['dolar_blue_compra'] = dolar_blue['compra']
        request.session['dolar_blue_venta'] = dolar_blue['venta']
    except:
        pass

    context = {}  
    

    if request.user.is_authenticated:    
        if request.GET.get('empresa'):
            empresa = request.GET.get('empresa')        
            try:
                empresa_obj = EmpresaRepresentada.objects.get(pk=empresa)
                request.session['empresa'] = empresa_obj.nombre
                request.session['empresa_cuit'] = empresa_obj.cuit
                request.session['empresa_pk'] = empresa_obj.pk

                empresa = request.session['empresa']                
                context['message'] = message
                context['empresa'] = empresa
            except EmpresaRepresentada.DoesNotExist:
                pass            


        if request.method == 'GET':
            try:
                empresas = EmpresaRepresentada.objects.filter(usuario=request.user)
                empresa = request.session.get('empresa')
                context['message'] = message
                context['empresa'] = empresa
                context['empresas'] = empresas
            except:
                pass

       


    return render(request,'index.html', context)

def changeEmpresa(request):
    print(request.GET)
    empresas = EmpresaRepresentada.objects.filter(usuario=request.user)
    context = {'empresas': ''}
    print(context)
    return render(request, index.html, context)

class EmpresaCreate(CreateView):
    model = EmpresaRepresentada
    form_class = EmpresaForm
    template_name = 'empresas/form_empresas.html'
    success_url = reverse_lazy('fyp:list-empresa')

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            obj_emp = form.save()
            obj_emp.usuario.add(request.user)
            
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Ingreso de nueva Empresa.'
        
        return context

class EmpresaList(ListView):
    model=EmpresaRepresentada
    template_name= 'empresas/list_empresa.html'
    
    def get_queryset(self):
        queryset = EmpresaRepresentada.objects.filter(usuario=self.request.user).order_by('-created_at')
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de empresas representadas.'

        return context

#------------- FIN INICIO ---------

#------------- PAGOS --------------
class PagoListView(ListView):
    model = Pagos
    template_name = 'pagos/pagos_list.html'

    def get_queryset(self):
        proveedor = self.request.GET.get('proveedor')
        emp_obj = EmpresaRepresentada.objects.get(pk=self.request.session['empresa_pk'])
        queryset = Pagos.objects.filter(titular=emp_obj).order_by('updated_at')        
        if proveedor:
            queryset = Pagos.objects.filter(proveedor__pk=proveedor)
        
        return queryset   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de pagos realizados'
        
        return context

class PagoCreateView(CreateView):
    model = Pagos
    form_class = PagoForm
    template_name = 'pagos/form_pagos.html'
    success_url = reverse_lazy('fyp:list-pagos')
   
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):        
        if request.method == 'POST':
            try:
                fact = request.POST.getlist('facturas')
                inst = request.POST.getlist('instrumentos')
            except:
                pass
            form = self.get_form()            
            if form.is_valid():
                '''facts = form.cleaned_data['facturas']
                insts = form.cleaned_data['instrumentos']'''                
                #cambio el estado de las facturas incluidas en el pago a true
                for f in fact: 
                    fc_obj = Factura.objects.get(id=f)  
                    fc_obj.estado_pago = True
                    fc_obj.save()
                #cambio el estado de los instrumentos incluidos en el pago a true
                for i in inst:
                    inst_obj = InstrumentoPago.objects.get(id=i)
                    inst_obj.estado_uilizado = True
                    inst_obj.save()
                

                form.save()
                return HttpResponseRedirect(self.success_url)          

            self.object = None
            context = self.get_context_data(**kwargs)
            context['message'] = 'Error'
            context['form'] = form 
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Ingreso de nuevo pago'
        context['form'] = self.form_class 
        context['empresa'] = self.request.session['empresa']        
        return context

class PagoDetailView(DetailView):
    model = Pagos
    template_name = 'pagos/pago_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'DETALLE DE PAGO'
        context['facturas'] = Factura.objects.filter(pagos=self.object)
        context['instrumentos'] = InstrumentoPago.objects.filter(pagos=self.object)
        context['empresa'] = self.request.session['empresa']
        return context

class PagoUpdateView(UpdateView):
    model = Pagos
    form_class = PagoForm
    template_name = 'pagos/form_pagos.html'
    success_url = reverse_lazy('fyp:list-pagos')
   
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)  

    

    def post(self, request, *args, **kwargs):
        fact = request.POST.getlist('facturas')
        inst = request.POST.getlist('instrumentos')
        form = self.get_form()
       
        if form.is_valid():
            #cambio el estado de las facturas incluidas en el pago a true
            for f in fact: 
                fc_obj = Factura.objects.get(id=f)  
                fc_obj.estado_pago = True
                fc_obj.save()
            #cambio el estado de los instrumentos incluidos en el pago a true
            for i in inst:
                inst_obj = InstrumentoPago.objects.get(id=i)
                inst_obj.estado_uilizado = True
                inst_obj.save()
            form.save()
            return HttpResponseRedirect(self.success_url)

        context = self.get_context_data(**kwargs)
        context['message'] = 'Error al actualizar'
        context['form'] = self.form_class
        return render(request, self.template_name, context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fc_list = Factura.objects.filter(pagos=self.object)
        ins_lst = InstrumentoPago.objects.filter(pagos=self.object)

        for fc in fc_list:
            fc.estado_pago = False
            fc.save()
        for ins in ins_lst:
            ins.estado_uilizado = False
            ins.save()
        context['message'] = 'Actualizar pago'
        context['form'] = self.form_class(instance=self.object)
        context['empresa'] = self.request.session['empresa']
        return context
        
class PagoDeleteView(DeleteView):
    model = Pagos
    success_url = reverse_lazy('fyp:list-pagos')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        fc_list = Factura.objects.filter(pagos=self.object)
        inst_list = InstrumentoPago.objects.filter(pagos=self.object)
        for fc in fc_list:
            fc.estado_pago = False
            fc.save()

        for inst in inst_list:
            inst.estado_uilizado = False
            inst.save()

        success_url = self.get_success_url()
        
        self.object.delete()

        return HttpResponseRedirect(success_url)  

# AJAX EL QUE MAS ME CONVENCE Y EL QUE MEJOR ENTIENDO
def load_datas(request):
    proveedor = request.GET.get('proveedor')
    fc = Factura.objects.filter(proveedor__pk__iexact=proveedor).exclude(estado_pago=True)
    ins = InstrumentoPago.objects.filter(proveedor__pk__iexact=proveedor).exclude(estado_uilizado=True)
    l = list(fc.values())
    for e in l:
        e['total'] = int([f.total for f in fc if f.id == e['id']][0])
    
    return JsonResponse({"facturas": l, "instrumentos": list(ins.values())}, safe=True)

#------------- FIN PAGOS ----------

#------------- FACTURAS --------------

class FacturasListView(ListView):
    success_url = reverse_lazy('fyp:list-facturas')
    template_name ='fc/facturas_list.html'    
    
    def get_queryset(self):
        cos = str(self.request.GET.get('cosecha'))
        proveedor = str(self.request.GET.get('proveedor'))
        rubro = str(self.request.GET.get('rubros'))
        
        emp_obj = EmpresaRepresentada.objects.get(pk=self.request.session['empresa_pk'])

        queryset = Factura.objects.filter(titular=emp_obj).order_by('-fecha_vto')
        
        
        if proveedor and proveedor != 'None':
            queryset = queryset.filter(proveedor__pk__iexact=proveedor)
        if cos and cos != 'None':
            queryset = queryset.filter(cosecha__iexact=cos)
        if rubro and rubro != 'None':
            queryset = queryset.filter(rubro__icontains=rubro)
        
        #queryset = [p for p in queryset if hasattr(p, 'notadedebito') and hasattr(p, 'notadecredito')]
        return queryset
    
    def get_context_data(self, **kwargs):
        if self.request.GET.get('empresa'):
            emp = EmpresaRepresentada.objects.get(pk=self.request.GET.get('empresa'))
            self.request.session['empresa'] = emp.nombre
            self.request.session['empresa_cuit'] = emp.cuit
            self.request.session['empresa_pk'] = emp.pk
            
        context = super().get_context_data(**kwargs)
        context['message'] = 'LISTADO DE FACTURAS'
        tot = round(sum([obj.total for obj in self.object_list]), 2)
        ftot = '{:,}'.format(tot)
        context['total_facturas'] = ftot
        context['rubros'] = set([obj.rubro for obj in self.object_list])
        context['lista_proveedores'] = set([obj.proveedor for obj in self.object_list])
        context['empresa'] = self.request.session['empresa']
        context['empresas'] = EmpresaRepresentada.objects.filter(usuario=self.request.user)
        return context

class FacturaCreateView(CreateView):
    model = Factura
    form_class = FacturaForm   
    template_name = 'fc/form_facturas.html'
    success_url = reverse_lazy('fyp:list-facturas')
    formset = ItemsFormset

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs): 
        if request.method == 'POST':            
            form = self.get_form()            
            if form.is_valid():
                emp_obj = EmpresaRepresentada.objects.get(pk=request.session['empresa_pk'])
                form.instance.titular = emp_obj
                fact_obj = form.save()
               
                formset = self.formset(request.POST, instance=fact_obj)
                if formset.is_valid():
                    formset.save()
                return HttpResponseRedirect(self.success_url)        

            self.object = None
            context = self.get_context_data(**kwargs)
            context['message'] = 'Error'
            context['form'] = form 
            context['formset'] = self.formset(request.POST)
            context['empresa'] = self.request.session['empresa']
            context['empresas'] = EmpresaRepresentada.objects.filter(usuario=self.request.user)
            return render(request, self.template_name, context)


    def get_context_data(self, **kwargs):
        if self.request.GET.get('empresa'):
            emp = EmpresaRepresentada.objects.get(pk=self.request.GET.get('empresa'))
            self.request.session['empresa'] = emp.nombre
            self.request.session['empresa_cuit'] = emp.cuit
            self.request.session['empresa_pk'] = emp.pk

        context = super().get_context_data(**kwargs)        
        context['message'] = 'Ingreso de nueva factura.'
        context['form'] = self.form_class 
        context['formset'] = self.formset   
        context['empresa'] = self.request.session['empresa']
        context['empresas'] = EmpresaRepresentada.objects.filter(usuario=self.request.user)
        return context
        
class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'fc/factura_detail.html'
    
    def get_context_data(self, **kwargs):
        if self.request.GET.get('empresa'):
            emp = EmpresaRepresentada.objects.get(pk=self.request.GET.get('empresa'))
            self.request.session['empresa'] = emp.nombre
            self.request.session['empresa_cuit'] = emp.cuit
            self.request.session['empresa_pk'] = emp.pk
        context = super().get_context_data(**kwargs)
        context['message'] = 'DETALLE DE FACTURA'
        context['items'] = ItemFactura.objects.filter(factura=self.object)
        context['empresa'] = self.request.session['empresa']
        context['empresas'] = EmpresaRepresentada.objects.filter(usuario=self.request.user)
       
        return context

class FacturaDeleteView(DeleteView):
    model= Factura
    success_url = reverse_lazy('fyp:list-facturas')

    def delete(self, request, *args, **kwargs):        
        obj = self.get_object()
        obj.delete()
        
        return HttpResponseRedirect(self.success_url)

class FacturaUpdateView(UpdateView):
    model = Factura
    form_class = FacturaForm   
    template_name = 'fc/form_facturas.html'
    success_url = reverse_lazy('fyp:list-facturas')
    formset = ItemsFormset

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):         
        form = self.get_form()    
        if form.is_valid():
            emp_obj = EmpresaRepresentada.objects.get(pk=request.session['empresa_pk'])
            form.instance.titular = emp_obj
            fact_obj = form.save()
            formset = self.formset(request.POST, instance=fact_obj)
            if formset.is_valid():
                formset.save()
            return HttpResponseRedirect(self.success_url)        

        
        context = self.get_context_data(**kwargs)
        context['message'] = 'Error'
        context['form'] = form 
        
        return render(request, self.template_name, context)
  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Actualizar factura.'
        context['form'] = self.form_class(instance=self.object)
        context['formset'] = self.formset(instance=self.object)
        context['empresa'] = self.request.session['empresa']
        context['empresas'] = EmpresaRepresentada.objects.filter(usuario=self.request.user)

        
        return context
        
#------------- FIN FACTURAS --------------

#------------- NOTAS --------------
class NotasCreditoCreateView(CreateView):
    model = NotaDeCredito
    form_class = FacturaForm   
    template_name = 'fc/form_facturas.html'
    success_url = reverse_lazy('fyp:list-facturas')
    formset = ItemsFormset

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs): 
        if request.method == 'POST':            
            form = self.get_form()            
            if form.is_valid():
                emp_obj = EmpresaRepresentada.objects.get(pk=request.session['empresa_pk'])
                form.instance.titular = emp_obj
                fact_obj = form.save()
                formset = self.formset(request.POST, instance=fact_obj)
                if formset.is_valid():
                    for e in formset:
                        e.instance.cantidad = e.instance.cantidad*-1
                    formset.save()
                return HttpResponseRedirect(self.success_url)        

            self.object = None
            context = self.get_context_data(**kwargs)
            context['message'] = 'Error'
            context['form'] = form 
            context['formset'] = self.formset(request.POST)
            context['empresa'] = self.request.session['empresa']
            context['empresas'] = EmpresaRepresentada.objects.filter(usuario=self.request.user)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        context['message'] = 'Ingreso de nueva nota de crédito.'
        context['form'] = self.form_class 
        context['formset'] = self.formset 
        context['empresa'] = self.request.session['empresa']
        return context

class NotasDebitoCreateView(CreateView):
    model = NotaDeDebito
    form_class = FacturaForm   
    template_name = 'fc/form_facturas.html'
    success_url = reverse_lazy('fyp:list-facturas')
    formset = ItemsFormset

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def post(self, request, *args, **kwargs): 
        if request.method == 'POST':            
            form = self.get_form()            
            if form.is_valid():
                emp_obj = EmpresaRepresentada.objects.get(pk=request.session['empresa_pk'])
                form.instance.titular = emp_obj
                fact_obj = form.save()
                formset = self.formset(request.POST, instance=fact_obj)
                if formset.is_valid():
                    formset.save()
                return HttpResponseRedirect(self.success_url)        

            self.object = None
            context = self.get_context_data(**kwargs)
            context['message'] = 'Error'
            context['form'] = form 
            context['formset'] = self.formset(request.POST)
            context['empresa'] = self.request.session['empresa']
            context['empresas'] = EmpresaRepresentada.objects.filter(usuario=self.request.user)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['message'] = 'Ingreso de nueva nota de débito.'
        context['form'] = self.form_class 
        context['formset'] = self.formset  
        context['empresa'] = self.request.session['empresa']

        return context

#------------- FIN FACTURAS --------------

#------------- INSTRUMENTOS PAGO --------------
class AddInstrumento(CreateView):
    model=InstrumentoPago
    form_class=InstrumentoPagoForm
    template_name = 'instrumentos/form_instrumentos.html'
    success_url = reverse_lazy('fyp:add-pagos')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Ingreso de nuevo metodo de pago'
          
        return context

class ListIntrumento(ListView):
    success_url = reverse_lazy('fyp:list-instrumentos')
    template_name ='instrumentos/instrumentos_list.html'

    def get_queryset(self):
        emp_obj = EmpresaRepresentada.objects.get(pk=self.request.session['empresa_pk'])
        query = InstrumentoPago.objects.filter(pagos__titular=emp_obj).order_by('-fecha_instrumento')
        
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'LISTA DE INSTRUMENTOS EMITIDOS'
        return context




#------------- FIN INSTRUMENTOS PAGO --------------

#-------------- PROVEEDORES -----------------------
class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/form_proveedor.html'
    success_url = reverse_lazy('fyp:list-proveedores')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)

        self.object = None
        context = self.get_context_data(**kwargs)
        context['message'] = 'Error'
        context['form'] = form 

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['message'] = 'Ingreso de nuevo proveedor'
        context['form'] = self.form_class         
        return context

class ProveedorDetailView(DetailView):
    model = Proveedor
    template_name = 'proveedores/proveedor_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'DETALLE DE PROVEEDOR'
    
        return context

class ListProveedorView(ListView):
    model = Proveedor
    template_name = 'proveedores/proveedor_list.html'

    def get_queryset(self):
        emp_obj = EmpresaRepresentada.objects.get(pk=self.request.session['empresa_pk'])
        queryset = list(set(Proveedor.objects.filter(factura__titular=emp_obj).order_by('nombre')))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de proveedores'

        return context

class ProveedorDeleteView(DeleteView):
    model= Proveedor
    success_url = reverse_lazy('fyp:list-proveedores')

    def delete(self, request, *args, **kwargs):        
        self.object = self.get_object()
        self.object.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm   
    template_name = 'proveedores/form_proveedor.html'
    success_url = reverse_lazy('fyp:list-proveedores')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        context['message'] = 'Actualizar proveedor'
        context['form'] = self.form_class(instance=self.object)
        return context   

#-------------- FIN PROVEEDORES --------------

#-------------- ARTICULOS --------------
class ArticuloCreate(CreateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'articulos/articulo_form.html'
    success_url = reverse_lazy('fyp:list-articulos')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)

        self.object = None
        context = self.get_context_data(**kwargs)
        context['message'] = 'Error'
        context['form'] = form 

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Ingreso de nuevo articulo'
        context['form'] = self.form_class 
        
        return context

class ArticuloListView(ListView):
    model = Articulo
    template_name = 'articulos/articulos_list.html' 
    queryset = Articulo.objects.all().order_by('nombre')

    def get_queryset(self):
        artic = self.request.GET.get('arti')
        if artic:
            self.queryset = Articulo.objects.filter(nombre__icontains=artic)

        return self.queryset

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de articulos'
        
        return context

class ArticuloDetailView(DetailView):
    model = Articulo
    template_name = 'articulos/articulo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'DETALLE DE ARTICULO'
    
        return context

class ArticuloDeleteView(DeleteView):
    model = Articulo
    success_url = reverse_lazy('fyp:list-articulos')   

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

class ArticuloUpdateView(UpdateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'articulos/articulo_form.html'
    success_url = reverse_lazy('fyp:list-articulos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Actualizar articulo'
        context['form'] = self.form_class(instance=self.object)
        return context

#-------------- FIN ARTICULOS --------------

#-------------- ITEM FACTURA --------------
class ItemFacturaDeleteView(DeleteView):
    model= ItemFactura

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()        
        id=str(self.object.factura.id)
        self.object.delete()
        success_url = f'../../{id}/detail_factura/'
        return HttpResponseRedirect(success_url)

#-------------- FIN ITEM FACTURA --------------

#-------------- CUENTAS CORRIENTES --------------
class CuentaCorrienteView(TemplateView):
    template_name = 'cuentas/cuentas_list.html'

    def get(self, request, *args, **kwargs):
        prov = ''
        context = self.get_context_data(**kwargs)
        if request.GET:
            try:
                prov = Proveedor.objects.get(pk=request.GET.get('proveedor'))                
                context['facturas'] = Factura.objects.filter(proveedor=prov).order_by('fecha')
                context['ncrs'] = NotaDeCredito.objects.filter(proveedor=prov).order_by('fecha')
                context['ndbs'] = NotaDeDebito.objects.filter(proveedor=prov).order_by('fecha')
                context['pagos'] = Pagos.objects.filter(proveedor=prov).order_by('fecha')
                context['message'] = f'MOVIMIENTOS {prov}'
                
                tot_fact = round(sum([obj.total for obj in context['facturas']]), 2) 
                tot_pagos = round(sum([obj.importe_instrumentos for obj in context['pagos']]), 2)
                context['saldos'] =  float(tot_fact)-float(tot_pagos)
                context['tot_pagos'] = float(tot_pagos)
                context['tot_cpm'] = float(tot_fact)
            except:
                pass

        return render(request, self.template_name, context)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'LISTADO CUENTA CORRIENTE'
        context['proveedores'] = Proveedor.objects.all()
        context['ncrs'] = NotaDeCredito.objects.all()
        context['ndbs'] = NotaDeDebito.objects.all()        
        context['facturas'] = Factura.objects.all()  
        context['pagos'] = Pagos.objects.all()  
        context['saldos'] = 0
        
        return context 
    
#--------------REPORTES---------------------------------
class ReporteComprobantes(ListView):
    model = Factura
    template_name = 'reportes/comprobantes.html'

    def get_queryset(self):
        queryset = Factura.objects.all()
        rubro = self.request.GET.get('rubros')
        cos = self.request.GET.get('cosecha')
        if rubro or cos:
            queryset = Factura.objects.filter(rubro__icontains=rubro).filter(cosecha__icontains=cos)
        return queryset

    def get_rubros(self):
        list_rubros = []
        lst = Factura.objects.all()
        for obj in lst:
            if obj.rubro not in list_rubros:
                list_rubros.append(obj.rubro)
        return 
        
    def get_totxrubro(self):
        queryset = self.model.objects.all()  
        '''for query in queryset:
            if query.rubro == 'COSECHA' or query.rubro == 'SERVICIOS DE COSECHA' or query.rubro == 'SERVICIO DE COSECHA':
                query.rubro = 'SERVICIO DE COSECHA'
                query.save()'''
        cosecha = self.request.GET.get('cosecha')  
        data = []
        rubros_list = []
        for query in queryset:
            if query.rubro not in rubros_list:
                rubros_list.append(query.rubro)
        for r in rubros_list:
            t = sum([obj.total for obj in Factura.objects.filter(cosecha__iexact=cosecha).filter(rubro__iexact=r)])
            d = dict(name=r, y=t)
            data.append(d)
        return data 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'REPORTE DE COMPROBANTES'
        context['rubros'] = self.get_rubros()
        context['totxrubros'] = self.get_totxrubro()
        return context


class ReporteCostos(TemplateView):
    template_name = 'reportes/costos.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        total_has = 621
        q = Pagos.objects.filter(facturas__cosecha__iexact='2021/2022')
        tot_p = sum([obj.importe_instrumentos for obj in q])
        tipo_cbio = 111.37
        context['costo'] = (tot_p/193)/tipo_cbio
        context['costo_tot'] = tot_p/tipo_cbio
        t_tri = sum([obj.kgs_finales() for obj in CartaDePorteDescargada.objects.filter(cp__cosecha__iexact='2021/2022')])
        context['tot_trigo'] = t_tri
        ven = 423789
        pen= t_tri-ven
        context['trigo_vendido'] = (ven/1000)*310
        context['trigo_pendiente'] = (pen/1000)*310

        cultivo = request.GET.get('cultivo')

        query_fc_semillas = ItemFactura.objects.filter(articulo__tipo__icontains='Semillas').filter(articulo__nombre__icontains=cultivo)
        query_fc_siembra = ItemFactura.objects.filter(articulo__tipo__icontains='Siembra').filter(articulo__nombre__icontains=cultivo)
        query_fc_agq = ItemFactura.objects.filter(articulo__tipo__icontains='Agroquimicos')
        lista_stock = set([obj.articulo.nombre for obj in ItemFactura.objects.filter(articulo__tipo__icontains='Agroquimicos')])
        dic_stock = {}
        lis_stock = []
        for el in lista_stock:
            suma = sum([obj.cantidad for obj in ItemFactura.objects.filter(articulo__tipo__icontains='Agroquimicos').filter(articulo__nombre__iexact=el)])          
            c_total = 0
            imp_total=0
            lis_pprom = []
            for obj in ItemFactura.objects.filter(articulo__tipo__icontains='Agroquimicos').filter(articulo__nombre__iexact=el):
                imp_total+=obj.cantidad*obj.precio_unitario
                c_total+=obj.cantidad
            p_prom = imp_total/c_total
            lis_pprom.append(dict(producto=el, precio_promedio=p_prom))
            lis_stock.append(dict(producto=el,cantidad=float(suma), p_promedio=p_prom))
            
        query_fc_fletes = sum([obj.precio_unitario for obj in ItemFactura.objects.filter(articulo__tipo__icontains='Fletes').filter(articulo__nombre__icontains=cultivo)])
        
        context['semillas'] = query_fc_semillas
        context['siembra'] = query_fc_siembra
        context['fletes'] = query_fc_fletes
        context['cultivo'] = cultivo
        context['agroq'] = query_fc_agq
        context['stock'] = lis_stock
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'REPORTE DE COSTOS'
       
        return context