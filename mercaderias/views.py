#! /usr/bin/env python3
import json

from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.template import loader

from django.db.models import Avg, Count, Min, Sum, Q

from comprobantes.models import EmpresaRepresentada, Factura, NotaDeDebito
from .models import *
from .forms import *

#from comprobantes.actualizacion import actualizarParte
# Create your views here.
#-----------CARTAS DE PORTE--------------------
from .datos import *
class ListaCp(ListView):
    model = CartaDePorte
    template_name = 'cpe/list_cp.html'
    #allow_empty = True
    #paginate_by = 10

    def get_queryset(self):
        emp_obj = EmpresaRepresentada.objects.get(pk=self.request.session['empresa_pk'])        
        queryset = CartaDePorte.objects.filter(titular=emp_obj).order_by('-created_at')
        
        try:
            producto = str(self.request.GET.get('producto'))
            cosecha = str(self.request.GET.get('cosecha'))
            informe = self.request.GET.get('informe')
            if producto != 'None' or cosecha != 'None':
                queryset = CartaDePorte.objects.filter(grano__icontains=producto, cosecha__contains=cosecha)
                if informe == 'on':
                    self.generarInforme(queryset, producto, cosecha)             
        except:
            pass
        
        return queryset
    
    def generarInforme(self, data, producto, cosecha):
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4, LETTER, landscape, portrait 
        w,h = landscape(A4)
        c = canvas.Canvas("reporte.pdf", pagesize=landscape(A4))
        c.drawImage("logoae.png", 700, h - 70, width=90, height=55)
        titulo = 'INFORME DE COSECHA'
        ml=50
        c.setFont("Helvetica", 15)
        c.drawString(ml+225,h-60, str(titulo))   
        c.setFont("Helvetica", 12)
        c.drawString(ml+20,h-80, f'Producto: {producto.upper()}')
        #----------ENCABEZADO----------------------------------------------------------------
        c.setFont("Helvetica", 10)
        c.drawString(ml+24,h-95, 'FECHA')
        c.drawString(ml+75,h-95, 'C.P.E.')
        c.drawString(ml+110,h-95, 'REM. COM.')
        c.drawString(ml+200,h-95, 'COMPRADOR')
        c.drawString(ml+280,h-95, 'DESTINO')
        c.drawString(ml+350,h-95, 'KGS.')
        c.drawString(ml+400,h-95, 'APLIC.')
        c.drawString(ml+460,h-95, 'CONTRATO')
        c.drawString(ml+530,h-95, 'CAMPO')
        count = 1
        
        c.line(ml+20,h-100,ml+600,h-100)
        for d in data:
            c.setFont("Helvetica",9)
            c.drawString(ml,h-110, f'{count}- ')            
            c.drawString(ml+25,h-110, str(d.fecha))
            c.drawString(ml+85,h-110, str(d.numero))
            if d.remitente_comercial:
                c.drawString(ml+110,h-110, str(d.remitente_comercial)[-15:])
            else:
                c.drawString(ml+120,h-110, '')
            c.drawString(ml+200,h-110, str(d.destinatario)[-16:])
            c.drawString(ml+280,h-110, str(d.destino.localidad))
            c.drawString(ml+350,h-110, str(d.peso_neto))
            try:
                cpd = CartaDePorteDescargada.objects.get(cp__ctg__iexact = d.ctg)
                c.drawString(ml+400,h-110, str(cpd.kgs_finales()))
                if cpd.contrato:
                    c.drawString(ml+460,h-110, str(cpd.contrato))
            except:
                c.drawString(ml+460,h-110, '')
                pass
            c.drawString(ml+530,h-110, str(d.direccion_procedencia))
            count+=1
            h-=15   
            if count%21 == 0:
                w,h = landscape(A4)
                c.drawImage("logoae.png", 700, h - 70, width=90, height=55)
                ml=50
                c.setFont("Helvetica", 15)
                c.drawString(ml+225,h-60, str(titulo))   
                c.setFont("Helvetica", 12)
                c.drawString(ml+20,h-80, f'Producto: {producto.upper()}')
                c.setFont("Helvetica", 10)
                c.drawString(ml+24,h-95, 'FECHA')
                c.drawString(ml+75,h-95, 'C.P.E.')
                c.drawString(ml+110,h-95, 'REM. COM.')
                c.drawString(ml+200,h-95, 'COMPRADOR')
                c.drawString(ml+280,h-95, 'DESTINO')
                c.drawString(ml+350,h-95, 'KGS.')
                c.drawString(ml+400,h-95, 'APLIC.')
                c.drawString(ml+460,h-95, 'CONTRATO')
                c.drawString(ml+530,h-95, 'CAMPO')        
                c.showPage()  
        
        cttos = ContratoMercaderia.objects.filter(producto__iexact=producto)
        alt = 130
        for ctto in cttos:
            if ctto.kgs_aplicados:
                c.setFont("Helvetica", 12)
                c.drawString(ml,h-alt, f'Total kilos aplicados al contrato {ctto.nro_vendedor}: {ctto.kgs_aplicados}')
                alt-=20   
        tot_kg_sin_ctto = 0
        for cp in data:
            cpd = CartaDePorteDescargada.objects.get(cp__pk=cp.pk)            
            if not cpd.contrato:
                tot_kg_sin_ctto+= cpd.kgs_finales()

        c.drawString(ml,h-alt-50, f'Total kilos sin contrato: {tot_kg_sin_ctto}')
        #c.drawString(ml,h-alt-50, f'Total kilos sin contrato: {tot_kg_sin_ctto}')
        kilos_totales = sum([obj.kgs_finales() for obj in CartaDePorteDescargada.objects.filter(cp__grano__iexact=producto).filter(cp__cosecha__iexact=cosecha)])
        c.drawString(ml,h-alt-80, f'Total kilos de {producto}: {kilos_totales}')

        c.save()
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de Cartas de Porte.'
        total=0
        for cp in self.object_list:
            try:
                total += float(cp.peso_neto)
            except:
                total += 0
        
        context['tns_totales'] = total/1000

        #dataExcel()

        return context

class CartaDePorteCreate(CreateView):
    model=CartaDePorte
    template_name = 'cpe/carta_create.html'
    form_class = CartaDePorteForm
    success_url = reverse_lazy('mer:lista-cp')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            emp_obj = EmpresaRepresentada.objects.get(pk=request.session['empresa_pk'])

            if form.is_valid():                
                form.instance.titular=emp_obj
                form.save()
                return HttpResponseRedirect(self.success_url)
           
        self.object = None
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Ingreso carta de porte.'
        return context

class DeleteCP(DeleteView):
    model= CartaDePorte
    success_url = reverse_lazy('mer:lista-cp')

    def delete(self, request, *args, **kwargs):     
        self.object = self.get_object()
        self.object.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

#-----------FIN CARTAS DE PORTE--------------------

#-----------APLICACIONES--------------------
class Aplicaciones(CreateView):
    model = CartaDePorteDescargada
    template_name = 'cpe/aplicacion_cp.html'
    form_class = CartaDePorteDescargadaForm
    success_url = reverse_lazy('mer:aplica-cp')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():                  
                if form.instance.contrato.nro_vendedor:
                    cp = CartaDePorte.objects.get(pk = form.instance.cp.pk)
                    cp.contrato = form.instance.contrato.nro_vendedor
                    cp.save()

                form.save()
                return HttpResponseRedirect(self.success_url)
           
        self.object = None
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['message'] = 'Aplicacion de cartas de porte.'
        
        return context

class DeleteAplicacion(DeleteView):
    model= CartaDePorteDescargada
    success_url = reverse_lazy('mer:lista-descargas-cp')

    def delete(self, request, *args, **kwargs):     
        self.object = self.get_object()
        self.object.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

class AplicacionesList(ListView):
    model = CartaDePorteDescargada
    template_name = 'cpe/list_cartadescargada.html'

    def get_queryset(self):        
        emp_obj = EmpresaRepresentada.objects.get(pk=self.request.session['empresa_pk'])        
        queryset = CartaDePorteDescargada.objects.filter(cp__titular=emp_obj).order_by('-created_at')     
        
        producto = str(self.request.GET.get('producto'))
        cosecha = str(self.request.GET.get('cosecha'))
        comprador = str(self.request.GET.get('comprador')) 
        establecimiento = str(self.request.GET.get('campo'))       
        
        if producto!= "None" and producto != " ":
            queryset = queryset.filter(cp__grano__icontains=producto)
        
        if comprador != "None" and comprador != " ":
            queryset = queryset.filter(cp__destinatario__pk=comprador)

        if cosecha != "None" and cosecha != " ":
            queryset = queryset.filter(cp__cosecha__icontains=cosecha)
        
        if establecimiento != "None" and establecimiento != " ":
            queryset = queryset.filter(cp__establecimiento__icontains=establecimiento)
        
        return queryset

    def get_lotes(self):
        lotes = []
        cps = CartaDePorte.objects.all()
        for cp in cps:
            if cp.direccion_procedencia not in lotes:
                lotes.append(cp.direccion_procedencia)        
        return lotes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de cartas de porte descargadas.'
        context['total_kgs_aplicados'] = sum([obj.kgs_finales() for obj in self.object_list])
        context['total_kgs_descargados'] = sum([obj.kilos_descargados for obj in self.object_list])
        context['compradores'] = Destinatario.objects.all()
        context['establecimientos'] = list(set([obj.cp.establecimiento for obj in self.object_list]))
        return context

class AplicacionesUpdateView(UpdateView):
    model = CartaDePorteDescargada
    form_class = CartaDePorteDescargadaForm
    template_name = 'cpe/aplicacion_cp.html'
    success_url = reverse_lazy('mer:lista-descargas-cp')       

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['message'] = 'Actualizar cp descargada'
        context['form'] = self.form_class(instance=self.object)
       
        return context
#-----------FIN APLICACIONES--------------------

#----------------CONTRATOS MERCADERIA-----------
class Contratos(CreateView):
    model = ContratoMercaderia
    template_name = 'ctos/contratos_mercaderias.html'
    form_class = ContratoMercaderiaForm
    success_url = reverse_lazy('mer:list-contratos-cp')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                
                form.save()
                return HttpResponseRedirect(self.success_url)
           
        self.object = None
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Ingreso de nuevo contrato'
        
        return context

class ContratosList(ListView):
    model = ContratoMercaderia
    template_name = 'ctos/list_contratos.html'
    
    
    def get_queryset(self):
        emp_obj = EmpresaRepresentada.objects.get(pk=self.request.session['empresa_pk'])        
        queryset = ContratoMercaderia.objects.filter(empresa=emp_obj).order_by('-created_at') 
        producto = str(self.request.GET.get('producto')).upper()        
        cosecha = str(self.request.GET.get('cosecha')).upper()
        comprador = str(self.request.GET.get('comprador')).upper()
        
        if producto != 'NONE' or comprador != 'NONE' or cosecha != 'NONE':
            queryset = ContratoMercaderia.objects.filter(producto__icontains=producto).filter(cosecha__icontains=cosecha).filter(comprador__pk__icontains=comprador)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de contratos realizados.'
        context['compradores'] = Destinatario.objects.all()

        return context

class ContratoDelete(DeleteView):
    model= ContratoMercaderia
    success_url = reverse_lazy('mer:list-contratos-cp')

    def delete(self, request, *args, **kwargs): 
        self.object = self.get_object()
        self.object.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

class ContratoDetail(DetailView):
    model = ContratoMercaderia
    template_name = 'ctos/contrato_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = f'Detalle Contrato {self.object.nro_comprador}'
        context['cartas'] = CartaDePorteDescargada.objects.filter(contrato=self.object).order_by('cp__fecha')
        context['pesificaciones'] = PesificacionContrato.objects.filter(contrato=self.object).order_by('fecha')
        context['total_kgs_pesificados'] = sum([obj.kilos_pesificados for obj in PesificacionContrato.objects.filter(contrato=self.object)])
        context['pendientes_pesificar'] = self.object.kgs_aplicados - context['total_kgs_pesificados']
        return context

#--------------FIJACIONES/PESIFICACIONES--------------
class CrearFijacion(CreateView):
    model = FijacionContrato
    template_name = 'ctos/fijaciones_contratos.html'
    form_class = FijacionContratoForm
    success_url = reverse_lazy('mer:list-contratos-cp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Ingreso de nueva fijacion'
        
        return context

class CrearPesificacion(CreateView):
    model = PesificacionContrato
    template_name = 'ctos/pesificaciones_contratos.html'
    form_class = PesificacionContratoForm
    success_url = reverse_lazy('mer:list-contratos-cp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Ingreso de nueva pesificacion'
        
        return context

#--------------FIN FIJACIONES/PESIFICACIONES----------

#----------------FIN CONTRATOS-----------

class Reportes(ListView):
    model = CartaDePorteDescargada
    template_name = 'reportes/reportes.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        try:
            producto = str(self.request.GET.get('producto'))   
            lote = str(self.request.GET.get('campo'))
            if lote == 'Del Sol':
                    lote = 'CORRAL DE BUSTOS'
            if lote == 'Vidaurre':
                lote = 'VIDAURRON'

            if producto != 'None':
                queryset = self.model.objects.filter(cp__grano__icontains=producto)
            if lote != 'None':                
                queryset = self.model.objects.filter(cp__direccion_procedencia__icontains=lote)
        except:
            pass
        
        return queryset
    
    def rindexcosxlote(self):
        #OBTENGO LA LISTA DE COSECHAS
        cosechas = self.get_cosechas()
        productos = ['SOJA', 'TRIGO', 'MAIZ']   
        establecimiento = str(self.request.GET.get('campo'))
        #cpos=Campo.objects.get(nombre__contains=establecimiento)
        #obtengo el total de produccion por lote por cultivo
        #print('pk br: ', cpos.pk)
        serie = []
        for prod in productos:
            lista_totxcos = []
            for cos in cosechas:
                suma = sum([cpd.kilos_descargados for cpd in CartaDePorteDescargada.objects.filter(cp__cosecha__icontains=cos).filter(cp__grano__icontains=prod).filter(cp__establecimiento__contains=establecimiento)])
                has = sum([pl.superficie_sembrada for pl in PlanSiembra.objects.filter(campania=cos).filter(cultivo=prod).filter(campo__nombre__icontains=establecimiento)])
               
                if suma == 0 or has == 0:
                    lista_totxcos.append(0)
                else:
                    lista_totxcos.append(suma/has)
            serie.append(dict(name=prod, data=lista_totxcos))   

        return serie
    
    def get_cosechas(self):       
        cosechas = []
        for cpd in self.object_list.order_by('cp__fecha'):
            if cpd.cp.cosecha not in cosechas:
                cosechas.append(cpd.cp.cosecha)
        #no se porque no devuelve una lista ordenada
        #en una sola linea resuelvo toda la funcion
        #prueba = list(set([obj.cp.cosecha for obj in self.object_list.order_by('cp__fecha')]))
        return cosechas

   
    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        context['message'] = 'Reporte de producción.'
        context['lista_campos'] = set([obj.cp.establecimiento.upper() for obj in self.object_list])
        context['listaxcosxlote'] = self.rindexcosxlote()
        context['lote'] = str(self.request.GET.get('campo'))
        context['cosechas'] = self.get_cosechas()
        #establecim()
        return context

class CuentaMercaderia(ListView):
    model = CartaDePorteDescargada
    template_name = 'reportes/cta_mercaderia.html'

    def get_queryset(self):        
        if self.request.method == 'GET':
            cosecha = self.request.GET.get('campania')
            queryset = CartaDePorteDescargada.objects.filter(cp__cosecha__iexact=cosecha)
        return queryset


    def get_kilos_totales(self):
        productos = list(set([obj.cp.grano for obj in self.get_queryset()]))
        data = []
        for producto in productos:
            tot = sum([obj.kgs_finales() for obj in self.object_list.filter(cp__grano=producto)])
            d=dict(producto= producto, total=tot)

            data.append(d)       
        return data

    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        campania = self.request.GET.get('campania')
        context['message'] = f'Detalle de producción campaña: {campania}.'
        context['campanias'] = list(set([obj.cp.cosecha for obj in CartaDePorteDescargada.objects.all()]))
        context['data'] = self.get_kilos_totales()
        return context
       
class PlanSiembraListView(ListView):
    model = PlanSiembra
    template_name = 'reportes/planes.html'

    def get_queryset(self):
        queryset = self.model.objects.all()  
        cosecha = self.request.GET.get('cosecha')      
        if cosecha:
            queryset = self.model.objects.filter(campania=cosecha)

        return queryset

    def get_hasxcos(self):
        queryset = self.model.objects.all()  
        cosecha = self.request.GET.get('cosecha')  
        has_soja = 0 
        has_maiz = 0 
        has_trigo = 0   
        data = []
        if cosecha:
            queryset = self.model.objects.filter(campania=cosecha)
            for plan in queryset:
                if plan.cultivo == 'SOJA':
                    has_soja += plan.superficie_sembrada
                if plan.cultivo == 'MAIZ':
                    has_maiz += plan.superficie_sembrada
                if plan.cultivo == 'TRIGO':
                    has_trigo += plan.superficie_sembrada
                
            d_soja = dict(name='SOJA', y=int(has_soja))
            d_trigo = dict(name='TRIGO', y=int(has_trigo))
            d_maiz = dict(name='MAIZ', y=int(has_maiz))   
            data.append(d_soja)
            data.append(d_trigo)
            data.append(d_maiz)    

        return data 

    def get_context_data(self, **kwargs):      
        cosecha = self.request.GET.get('cosecha')  
        context = super().get_context_data(**kwargs)
        context['message'] = f'Campaña: {cosecha}.'
        context['hasxcos'] = self.get_hasxcos()
        return context

#--------------LABORES----------
class OrdenDeLaborCreate(CreateView):
    model = OrdenDeLabor
    form_class = OrdenDeLaborForm   
    template_name = 'labor/form_orden_de_labor.html'
    success_url = reverse_lazy('mer:listar-labor')
    formset = ItemsFormset

    def get(self, request, *args, **kwargs):
        epk = request.session['empresa']
        
        emp_obj = EmpresaRepresentada.objects.get(nombre__iexact=epk)
        campos_qs = Campo.objects.filter(empresa=emp_obj)
        if len(campos_qs)<1:
            #REDIRIJO A OTRA PAGINA PARA CARGAR LOS CAMPOS
            #YA QUE LA EMPRESA NO TIENE CAMPOS AGREGADOS
            return redirect('fyp:index')
       
        return render(request,self.template_name, {'form':self.form_class(initial={'campos': campos_qs}), 'formset': self.formset})

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs): 
        if request.method == 'POST':     
            form = self.get_form()
            if form.is_valid():
                emp_obj = EmpresaRepresentada.objects.get(pk=self.request.session['empresa_pk'])
                form.instance.titular = emp_obj
                ol_obj = form.save()
                formset = self.formset(request.POST, instance=ol_obj)
                if formset.is_valid(): 
                    formset.save()
                
                return HttpResponseRedirect(self.success_url)      

            self.object = None
            context = self.get_context_data(**kwargs)
            context['message'] = 'Error'
            context['form'] = form 
            context['formset'] = self.formset(request.POST)
            
            return render(request, self.template_name, context)

    def add_formset(self):
        lst = [self.formset]
        return lst

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Ingreso Orden de Labor.'
        context['form'] = self.form_class 
        context['formset'] = self.add_formset()  

        return context

class OrdenDeLaborList(ListView):
    model = OrdenDeLabor
    template_name = 'labor/list_ordenes_labor.html'

    def get_queryset(self):
        emp_obj = EmpresaRepresentada.objects.get(pk=self.request.session['empresa_pk'])        
        queryset = OrdenDeLabor.objects.filter(titular=emp_obj).order_by('-created_at') 
        
        return queryset


    @property
    def genera_totales(self):
        emp_obj = EmpresaRepresentada.objects.get(pk=self.request.session['empresa_pk']) 
        lista_articulos = list(set([obj.insumo for obj in ItemLabor.objects.filter(orden__titular=emp_obj)])) 
        tot = []
        for artic in lista_articulos:
            suma = 0
            for obj in self.object_list:
                for k in obj.total_ismo:
                    if k['producto']==artic:
                        suma+=k['total']
        
            d= dict(a=artic, tt=round(suma, 2)) 
            tot.append(d)          
        return tot

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Lista Ordenes de Labor.'
        context['totales'] = self.genera_totales
        return context

class OrdenDeLaborDelete(DeleteView):
    model=OrdenDeLabor
    success_url = reverse_lazy('mer:listar-labor')
    def delete(self, request, *args, **kwargs): 
        self.object = self.get_object()
        self.object.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

#--------------FIN LABORES----------
def listadoStock(request):  
    template = loader.get_template('stock/stock.html')
    tp=request.GET.get('tipo')
    if tp:
        tot, tot_usado, final = tipo_producto_stock(request,tp)
    else:
        tp='AGROQUIMICOS'
        tot, tot_usado, final = tipo_producto_stock(request,tp)
        
    
    context = {
        'message': f'STOCK DE {tp}',
        'totales_stock': tot,
        'totales_stock_usados': tot_usado,
        'saldo_final': final
    }
    
    return HttpResponse(template.render(context, request))

def tipo_producto_stock(request,data):
    tot, tot_usado = returnRequestStock(request,data,'2021/2022')    
    final = []
    lst_art_usados = list(set([obj['articulo'] for obj in tot_usado]))
    for d in tot:
        suma_usado = 0
        if d['articulo'] in lst_art_usados:
            suma_usado += sum([obj['total_usado'] for obj in tot_usado if obj['articulo']==d['articulo']])

        saldo = round(float(d['total']) - float(suma_usado), 2)
        dic = dict(articulo=d['articulo'], s=saldo)
        final.append(dic)
    return tot, tot_usado, final

def returnRequestStock(request,data1, data2):    

    emp_obj = EmpresaRepresentada.objects.get(pk=request.session['empresa_pk'])
    latest_question_list = ItemFactura.objects.filter(factura__titular=emp_obj, factura__rubro__iexact=data1, factura__cosecha__iexact=data2)\
    .exclude(articulo__nombre__iexact='Test').exclude(articulo__nombre__iexact='Intereses').exclude(articulo__nombre__iexact='ART24COVEI')

    if data1 == 'AGROQUIMICOS':
        lista_queries_items = ItemLabor.objects.filter(orden__labor__icontains='FUMIGACION',orden__campania__iexact=data2)
    if data1 == 'SEMILLAS':
        lista_queries_items = ItemLabor.objects.filter(orden__labor__icontains='SIEMBRA',orden__campania__iexact=data2)
    if data1 == 'FERTILIZANTES':
        lista_queries_items = ItemLabor.objects.filter(orden__labor__icontains='FERTILIZACION',orden__campania__iexact=data2)
    
    lista_articulos = list(set([obj.articulo for obj in latest_question_list]))
    lista_items_articulos = list(set([obj.insumo for obj in lista_queries_items]))
   
    tot_stock = []
    for art in lista_articulos:
        tot_art = dict(articulo=art, facts=list([obj.factura for obj in latest_question_list.filter(articulo=art)]), total=sum(obj.cantidad for obj in latest_question_list.filter(articulo=art)))
        tot_stock.append(tot_art)
    tot_stock_usado = []
   
    for art in lista_items_articulos:
        tt = ItemLabor.objects.filter(insumo__nombre__iexact=art)
        suma = 0
        for i in tt:
            ol = i.orden            
            suma+= round(i.dosis*ol.total_has, 2)
        d=dict(articulo=art, total_usado=suma)
       
        tot_stock_usado.append(d)
        
    return tot_stock, tot_stock_usado

#-------------- LOTES ---------
# VERBOS READ CREATE UPDATE AND DELETE
class ListaLotes(ListView):
    template_name = 'arrendamientos/lista_lotes.html'

    def get_queryset(self):
        emp_obj = EmpresaRepresentada.objects.get(nombre=self.request.session['empresa'])
        query = Lote.objects.filter(campo__empresa__pk=emp_obj.pk).order_by('campo')

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'LISTA LOTES POR CAMPO'
        context['total_has'] = round(sum([obj.hectareas for obj in self.object_list]), 2)
        return context

class CreateLote(CreateView):
    template_name = 'arrendamientos/create_lote.html'
    model = Lote
    form_class = LoteForm
    success_url = reverse_lazy('mer:listar-lotes')
   
    def get(self, request, *args, **kwargs):
        epk = request.session['empresa']        
        emp_obj = EmpresaRepresentada.objects.get(nombre__iexact=epk)
        campos_qs = Campo.objects.filter(empresa=emp_obj)
        prov = [obj.proveedor for obj in Factura.objects.filter(titular=emp_obj)]
        
        if len(campos_qs)<1 or len(prov)<1:
            #REDIRIJO A OTRA PAGINA PARA CARGAR LOS CAMPOS O PROPIETARIOS
            #YA QUE LA EMPRESA NO TIENE CAMPOS AGREGADOS
            
            error_campos = 'DEBE INGRESAR CAMPOS'
            return render(request,self.template_name, {'error_campos': error_campos})
        
       
        return render(request,self.template_name, {'form':self.form_class(initial={'campo': campos_qs, 'propietario': prov}), 'message':'CREAR LOTE EN CAMPO'})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'CREAR LOTE EN CAMPO'
        return context
#-------------- ARRENDAMIENTOS ---------
# VERBOS CREATE UPDATE AND DELETE
class ListaArrendamiento(ListView):
    template_name = 'arrendamientos/lista_arrendamientos.html'

    def get_queryset(self):
        emp_obj = EmpresaRepresentada.objects.get(nombre=self.request.session['empresa'])
        query = Arrendamiento.objects.filter(empresa__pk=emp_obj.pk).order_by('fecha_fin')

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'LISTA CONTRATOS DE ARRENDAMIENTO'
        context['total_has'] = round(sum([obj.lote.hectareas for obj in self.object_list]), 2)
        return context

class CrearArrendamiento(CreateView):
    model = Arrendamiento
    form_class = ContratoArrendamientoForm
    template_name = 'arrendamientos/crear_arrendamiento.html'
    success_url = reverse_lazy('mer:listar-arrendamientos')

    def get(self, request, *args, **kwargs):
        epk = request.session['empresa_pk']        
        emp_obj = EmpresaRepresentada.objects.get(pk=epk)
        campos_qs = Lote.objects.filter(campo__empresa=emp_obj)
        prov = [obj.proveedor for obj in Factura.objects.filter(titular=emp_obj)]
        
        if len(campos_qs)<1 or len(prov)<1:
            #REDIRIJO A OTRA PAGINA PARA CARGAR LOS CAMPOS O PROPIETARIOS
            #YA QUE LA EMPRESA NO TIENE CAMPOS AGREGADOS
            
            error_campos = 'LA EMPRESA DEBE TENER ARRENDADOR COMO PROVEEDOR O LOTES INGRESADOS'
            return render(request,self.template_name, {'error_campos': error_campos})        
       
        return render(request,self.template_name, {'form':self.form_class(initial={'lote': campos_qs, 'arrendador': prov}), 'message':'INGRESAR CONTRATO DE ARRENDAMIENTO'})
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                emp_obj = EmpresaRepresentada.objects.get(pk=request.session['empresa_pk'])
                form.instance.empresa = emp_obj
                form.save()
                return HttpResponseRedirect(self.success_url)

            self.object = None
            context = self.get_context_data(**kwargs)
            context['message'] = 'Error'
            context['form'] = form             
            
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'INGRESAR CONTRATO DE ARRENDAMIENTO'
        return context

class EliminarArrendamiento(DeleteView):
    model=Arrendamiento
    success_url = reverse_lazy('mer:listar-arrendamientos')
    def delete(self, request, *args, **kwargs): 
        self.object = self.get_object()
        self.object.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
