#! /usr/bin/env python3

from django.db import models
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Empresa(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    cuit = models.IntegerField(unique=True)
    usuario = models.ManyToManyField(User, related_name="empresas")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return f'{self.nombre}'

class EmpresaRepresentada(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    cuit = models.IntegerField(unique=True)
    usuario = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    cuit = models.IntegerField(unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


    def __str__(self):
        return f'{self.nombre}'

class Articulo(models.Model):
    VARIOS = 'VARIOS'
    COMBUSTIBLE='COMBUSTIBLE'
    SEMILLAS = 'SEMILLAS'
    AGROQUIMICOS = 'AGROQUIMICOS'
    COSECHA='COSECHA'
    SIEMBRA='SIEMBRA'
    FERTILIZACION='FERTILIZACION'
    LABORES_VARIAS='LABORES_VARIAS'
    FUMIGACION='FUMIGACION'
    DIF_DE_CAMBIO = 'DIF_DE_CAMBIO'
    AJUSTE = 'AJUSTE'
    INTERESES = 'INTERESES'
    ART24COVEI = 'ART24COVEI'
    ARRENDAMIENTO='ARRENDAMIENTO'
    FLETES = 'FLETES'
    CHOICES_TYPE = [(FLETES,'FLETES'),(ART24COVEI,'ART24COVEI'),(INTERESES, 'INTERESES'),(SEMILLAS, 'Semillas'),(ARRENDAMIENTO, 'Arrendamiento'),(FUMIGACION, 'Fumigación'),(LABORES_VARIAS, 'Labores Varias'), (FERTILIZACION, 'Fertilización'), (AGROQUIMICOS,'Agroquimicos'), (COSECHA, 'Cosecha'),(SIEMBRA, 'Siembra'), (DIF_DE_CAMBIO,'Dif. de cambio'), (AJUSTE,'Ajuste'), (VARIOS, 'Varios'), (COMBUSTIBLE, 'Combustible')]
    
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255, choices=CHOICES_TYPE, default=VARIOS)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Articulos"
        verbose_name_plural = "Articulos"

    def __str__(self):
        return f'{self.nombre}'

class Factura(models.Model):
    VARIOS = 'VARIOS'
    AGROQUIMICOS = 'AGROQUIMICOS'
    FLETES = 'FLETES'
    FERTILIZANTES = 'FERTILIZANTES'
    SEMILLAS = 'SEMILLAS'
    LABORES = 'LABORES'
    DIF_DE_CAMBIO = 'DIF_DE_CAMBIO'
    INTERESES = 'INTERESES'
    HONORARIOS = 'HONORARIOS'
    SERVICIOS = 'SERVICIOS'
    COMBUSTIBLE = 'COMBUSTIBLE'
    ARRENDAMIENTOS = 'ARRENDAMIENTOS'    
    RUBRO_TYPE = [(VARIOS,'Varios'), (FLETES, 'Fletes'),(AGROQUIMICOS,'Agroquimicos'), (FERTILIZANTES, 'Fertilizantes'), (SEMILLAS, 'Semillas'), (LABORES, 'Labores'), (DIF_DE_CAMBIO,'Dif. de cambio'), (INTERESES, 'Intereses'), (HONORARIOS, 'Honorarios'), (SERVICIOS, 'Servicios'), (COMBUSTIBLE, 'Combustible'), (ARRENDAMIENTOS, 'Arrendamientos')]
    
    COS20152016="2015/2016"
    COS20162017="2016/2017"
    COS20172018="2017/2018"
    COS20182019="2018/2019"
    COS20192020="2019/2020"
    COS20202021="2020/2021"
    COS20212022="2021/2022"
    COS20222023="2022/2023"
    COS20232024="2023/2024"
    COS20242025="2024/2025"
    COSECHAS=[(COS20152016,"2015/2016"), (COS20162017,"2016/2017"), (COS20172018,"2017/2018"), \
        (COS20182019,"2018/2019"),(COS20192020,"2019/2020"),(COS20202021,"2020/2021"),\
        (COS20212022, "2021/2022"), (COS20222023, "2022/2023"), (COS20232024, "2023/2024"), (COS20242025, "2024/2025")]

    fecha = models.DateField()
    fecha_vto = models.DateField()
    numero = models.CharField(max_length=255)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    titular = models.ForeignKey(EmpresaRepresentada, on_delete=models.CASCADE, null=True, blank=True)
    
    tipo_cambio = models.DecimalField(null=True, blank=True, max_digits=30, decimal_places=4, default=0)
    impuesto = models.DecimalField(null=True, blank=True, max_digits=30, decimal_places=2, default=0)
    otro_importe = models.DecimalField(null=True, blank=True, max_digits=30, decimal_places=2, default=0)
    rubro = models.CharField(max_length=255, choices=RUBRO_TYPE, default=VARIOS)
    estado_pago = models.BooleanField(null=True, blank=True, default=False)
    cosecha = models.CharField(max_length=255, choices=COSECHAS, default=COS20212022)

    ventas = models.BooleanField(null=True, blank=True, default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

    
    @property
    def subtotal(self):
        try:
            subtotal = sum([obj.precio_unitario*obj.cantidad for obj in ItemFactura.objects.filter(factura=self)])
        except:
            subtotal = 0
        return round(subtotal, 2)

    @property
    def imp(self):
        if(self.impuesto == None):
            self.impuesto = 0.0
        i = self.subtotal*(self.impuesto/100)        
        return round(i, 2)
    
    @property
    def total(self):
        if(self.otro_importe == None):
            self.otro_importe = 0.0
        if(self.tipo_cambio == None):
            self.tipo_cambio = 0.0
        
        if self.tipo_cambio:
            tt = (float(self.subtotal)+float(self.imp)+float(self.otro_importe))*float(self.tipo_cambio)
        else:
            tt = float(self.subtotal)+float(self.imp)+float(self.otro_importe)
        
        return round(tt, 2) 

    @property
    def total_usd(self):
        if(self.otro_importe == None):
            self.otro_importe = 0.0
        
        if(self.tipo_cambio == None):
            self.tipo_cambio = 0.0
        
        if self.tipo_cambio == 0:
            tt = 0
        else:
            tt = float(self.subtotal)+float(self.imp)+float(self.otro_importe)
        
        return round(tt, 2) 

    @property
    def estado(self):
        if self.estado_pago:
            return 'PAGADA'
        else:
            return 'PENDIENTE'

    def __str__(self):
        return f'Numero: {self.numero} - Proveedor: {self.proveedor} - Total: {self.total}'

class NotaDeCredito(Factura):
    
    tipo='Nota de Crédito'

    class Meta:
        verbose_name = "Nota de Crédito"
        verbose_name_plural = "Notas de Crédito"
    
class NotaDeDebito(Factura):
   
    tipo='Nota de Débito'   

    class Meta:
        verbose_name = "Nota de Débito"
        verbose_name_plural = "Notas de Débito" 

class ItemFactura(models.Model):
    articulo = models.ForeignKey(Articulo, models.SET_DEFAULT, null=True, blank=True, default='VARIOS')
    cantidad = models.DecimalField(null=True, blank=True,max_digits=30, decimal_places=2)
    precio_unitario = models.DecimalField(null=True, blank=True,max_digits=30, decimal_places=4)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, null=True, blank=True, related_name='item')

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
    
    @property
    def subtotal(self):
        if self.cantidad and self.precio_unitario:
            st = self.cantidad*self.precio_unitario
        else:
            st = 0
        return round(st, 2) 


    def __str__(self):
        return f'Articulo: {self.articulo} - Cantidad: {self.cantidad} - Subtotal: {self.subtotal}'

class InstrumentoPago(models.Model):
    CHEQUE = 'CHEQUE'
    E_CHEQ = 'E-CHEQ'
    TARJETA = 'TARJETA'
    TRANSFERENCIA = 'TRANSFERENCIA'
    EFECTIVO = 'EFECTIVO'
    INSTRUMENTOS_TYPE=[(CHEQUE, 'Cheque'), (E_CHEQ, 'E-cheq'), (TARJETA, 'Tarjeta'), (TRANSFERENCIA, 'Transferencia'), (EFECTIVO,'Efectivo') ]
    
    MACRO ='MACRO'
    GALICIA = 'GALICIA'
    CAJA = 'CAJA'
    INSTITUCION =[(MACRO, 'Macro'), (GALICIA,'Galicia'), (CAJA, 'Caja')]
    
    fecha = models.DateField(null=True, blank=True)
    instrumento = models.CharField(max_length=255, choices=INSTRUMENTOS_TYPE, default=CHEQUE)
    numero_instrumento = models.CharField(max_length=255, blank=True)
    fecha_instrumento = models.DateField(null=True, blank=True)
    institucion_instrumento = models.CharField(max_length=255, choices=INSTITUCION, default=MACRO)
    importe = models.DecimalField(null=True, blank=True,max_digits=10, decimal_places=2)
    
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    estado_uilizado = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def estado(self):
        if self.estado_uilizado:
            return 'UTILIZADO'
        else:
            return 'SIN ASIGNAR'

    
    def __str__(self):
        return f'{self.id} - {self.proveedor} - {self.numero_instrumento} - {self.instrumento} - {self.importe} - {self.estado}'

class Pagos(models.Model):
    fecha = models.DateField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    instrumentos = models.ManyToManyField(InstrumentoPago, related_name='pagos')
    facturas = models.ManyToManyField(Factura, related_name='pagos')
    numero = models.CharField(max_length=255, default='0')
    titular = models.ForeignKey(EmpresaRepresentada, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def _items_dict(self):
        items_dict = {}

        qs_instrumento_pago = InstrumentoPago.objects.filter(pagos=self)

        for instrumento_obj in qs_instrumento_pago:
            items_dict[instrumento_obj.pk] = instrumento_obj

        return items_dict

    @property
    def importe_instrumentos(self):        
        return round(float(sum([item.importe for item in self._items_dict.values()])), 2)

    @property
    def _items_fact_dict(self):
        items_dict = {}

        qs_facturas_pago = Factura.objects.filter(pagos=self)

        for factura_obj in qs_facturas_pago:
            items_dict[factura_obj.pk] = factura_obj

        return items_dict

    @property
    def importe_facturas(self):
        return round(sum([item.total for item in self._items_fact_dict.values()]), 2)
   
    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    
    def __str__(self):
        return f'{self.id} - {self.fecha} - {self.importe_instrumentos} - {self.importe_facturas}'

