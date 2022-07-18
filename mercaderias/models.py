#! /usr/bin/env python3
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from comprobantes.models import *

SOJA="SOJA"
TRIGO="TRIGO"
MAIZ="MAIZ"
GIRASOL="GIRASOL"
SORGO="SORGO"
PRODUCTO_TYPE=[(SOJA, "soja"), (MAIZ, "maíz"), (TRIGO, "trigo"), (GIRASOL, "girasol"), (SORGO, "sorgo")]
#COSECHA
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
COSECHAS=[(COS20152016,"2015/2016"), (COS20162017,"2016/2017"), (COS20172018,"2017/2018"), (COS20182019,"2018/2019"),(COS20192020,"2019/2020"),(COS20202021,"2020/2021"),(COS20212022, "2021/2022"), (COS20222023, "2022/2023"), (COS20232024, "2023/2024"), (COS20242025, "2024/2025")]

# Create your models here.
#--------------PARTE DE CP------------------------------
class Intermediario(models.Model):
    nombre = models.CharField(max_length=255)
    cuit = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    #funcion para devolver el nombre de usuario que se agrega al serializer
    #def nombreUser(self):
      #  return self.user.nombre

class RemitenteComercial(models.Model):
    nombre = models.CharField(max_length=255)
    cuit = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    #funcion para devolver el nombre de usuario que se agrega al serializer
    #def nombreUser(self):
      #  return self.user.nombre

class Corredor(models.Model):
    nombre = models.CharField(max_length=255)
    cuit = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    #funcion para devolver el nombre de usuario que se agrega al serializer
    #def nombreUser(self):
      #  return self.user.nombre

class MercadoATermino(models.Model):
    nombre = models.CharField(max_length=255)
    cuit = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    #funcion para devolver el nombre de usuario que se agrega al serializer
    #def nombreUser(self):
      #  return self.user.nombre

class Destinatario(models.Model):
    nombre = models.CharField(max_length=255)
    cuit = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    #funcion para devolver el nombre de usuario que se agrega al serializer
    #def nombreUser(self):
      #  return self.user.nombre

class Destino(models.Model):
    destinatario = models.ForeignKey(Destinatario, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=255)
    cuit = models.CharField(max_length=255)
    codigo_de_planta = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    localidad = models.CharField(max_length=255)
    provincia = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    #funcion para devolver el nombre de usuario que se agrega al serializer
    #def nombreUser(self):
      #  return self.user.nombre

class IntermediarioFlete(models.Model):
    nombre = models.CharField(max_length=255)
    cuit = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    #funcion para devolver el nombre de usuario que se agrega al serializer
    #def nombreUser(self):
      #  return self.user.nombre

class Transportista(models.Model):
    nombre = models.CharField(max_length=255)
    cuit = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    #funcion para devolver el nombre de usuario que se agrega al serializer
    #def nombreUser(self):
      #  return self.user.nombre

class Chofer(models.Model):
    transportista = models.ForeignKey(Transportista, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    cuit = models.CharField(max_length=255)
    patente_chasis = models.CharField(max_length=255)
    patente_acoplado = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.apellido, self.nombre)
    # funcion para devolver el nombre de usuario que se agrega al serializer
    # def nombreUser(self):
      #  return self.user.nombre

class Entregador(models.Model):
    nombre = models.CharField(max_length=255)
    cuit = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    #funcion para devolver el nombre de usuario que se agrega al serializer
    #def nombreUser(self):
      #  return self.user.nombre

class ContratoMercaderia(models.Model):  
    #TIPOS DE CONTRATO
    A_FIJAR="FIJAR"  
    FORWARD="FORWARD"
    DISPONIBLE="DISPONIBLE"
    TIPOS_CTO = [(A_FIJAR, "A fijar"), (FORWARD, "Forward"), (DISPONIBLE, "Disponible")]
    
    fecha_contrato = models.DateField()
    nro_comprador = models.CharField(max_length=20)
    nro_vendedor = models.CharField(max_length=20)
    empresa = models.ForeignKey(EmpresaRepresentada, on_delete=models.CASCADE)
    comprador = models.ForeignKey(Destinatario, on_delete=models.CASCADE)
    tipo_contrato = models.CharField(max_length=100, choices=TIPOS_CTO)
    producto = models.CharField(max_length=20, choices=PRODUCTO_TYPE, default=SOJA)
    kilos_pactados = models.PositiveBigIntegerField()
    cosecha = models.CharField(max_length=60, choices=COSECHAS)
    precio = models.PositiveIntegerField()
    fecha_inicio_cumplimiento = models.DateField()
    fecha_fin_cumplimiento = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        app_label = 'mercaderias'
        managed = True
    #PROBAR DE ENTRADA
    @property
    def kgs_pendientes(self):
        kgs = self.kilos_pactados - sum([int(obj.kgs_finales()) for obj in CartaDePorteDescargada.objects.filter(contrato=self)])
        return kgs

    @property
    def kgs_aplicados(self):
        kgs = sum([int(obj.kgs_finales()) for obj in CartaDePorteDescargada.objects.filter(contrato=self)])
        return kgs

    def __str__(self):
        return self.nro_vendedor

class Campo(models.Model):     
    hectareas = models.FloatField()
    nombre = models.CharField(max_length=255)
    localidad = models.CharField(max_length=255)
    provincia = models.CharField(max_length=255)
    empresa = models.ForeignKey(EmpresaRepresentada, on_delete=models.CASCADE, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta: 
        app_label = 'mercaderias'
        managed = True

    def __str__(self):
        return self.nombre

class CartaDePorte(models.Model):
    SANTA_FE = "Santa fe"
    CORDOBA = "Cordoba"
    PROVINCIAS = [(SANTA_FE, "Santa Fe"), (CORDOBA, "Córdoba")]
    MARIA_TERESA="Maria Teresa"
    SAN_GREGORIO = "San Gregorio"
    TEODELINA="Teodelina"
    CORRAL="Corral de Bustos"
    LOCALIDADES = [(CORRAL, "Corral de Bustos"),(MARIA_TERESA,"M. Teresa"),(SAN_GREGORIO,"Sn. Gregorio"),(TEODELINA,"Teodelina")]
    Z_RURAL="Zona Rural S/N"
    B_RODRIGUEZ = "Benjamin Rodriguez"
    VIDAURRE = "Vidaurre"
    S_ENRIQUE = "San Enrique"
    SILIONI = "Silioni"
    DEL_SOL = "Del Sol"
    
    ESTABLECIMIENTOS = [(SILIONI,"Silioni"),(S_ENRIQUE,"San Enrique"),(VIDAURRE,"Vidaurre"),
    (B_RODRIGUEZ,"Benjamin Rodriguez"),(DEL_SOL,"Del Sol")]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    numero = models.CharField(max_length=255, null=True, blank=True)
    ctg = models.CharField(max_length=255, null=True, blank=True)
    renspa = models.CharField(max_length=255, null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    titular = models.ForeignKey(EmpresaRepresentada, on_delete=models.CASCADE, null=True, blank=True)
    intermediario = models.ForeignKey(Intermediario, on_delete=models.CASCADE, null=True, blank=True)
    remitente_comercial = models.ForeignKey(RemitenteComercial, on_delete=models.CASCADE, null=True, blank=True)
    corredor_comprador = models.ForeignKey(Corredor, on_delete=models.CASCADE, null=True, blank=True, related_name='corredorC')
    mercado_a_termino = models.ForeignKey(MercadoATermino, on_delete=models.CASCADE, null=True, blank=True)
    corredor_vendedor = models.ForeignKey(Corredor, on_delete=models.CASCADE, null=True, blank=True, related_name='corredorV')
    entregador = models.ForeignKey(Entregador, on_delete=models.CASCADE, null=True, blank=True)
    destinatario = models.ForeignKey(Destinatario, on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
    destino = models.ForeignKey(Destino, on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
    intermediario_flete = models.ForeignKey(IntermediarioFlete, on_delete=models.CASCADE, null=True, blank=True)
    transportista = models.ForeignKey(Transportista, on_delete=models.CASCADE, null=True, blank=True)
    chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE, null=True, blank=True)
    grano = models.CharField(max_length=255, choices=PRODUCTO_TYPE, default=SOJA)
    tipo = models.CharField(max_length=255, null=True, blank=True)
    cosecha = models.CharField(max_length=255, choices=COSECHAS, default=COS20212022)
    contrato = models.CharField(max_length=255, null=True, blank=True) #aca enlazamos con los ctos. de compra vta.
    pesada_en_destino = models.BooleanField(null=True, blank=True)
    kgs_estimados = models.BooleanField(null=True, blank=True)
    declaracion_calidad = models.BooleanField(null=True, blank=True)
    conforme = models.BooleanField(null=True, blank=True)
    condicional = models.BooleanField(null=True, blank=True)
    peso_bruto = models.CharField(max_length=255, null=True, blank=True)
    peso_tara = models.CharField(max_length=255, null=True, blank=True)
    peso_neto = models.CharField(max_length=255, null=True, blank=True)
    observaciones = models.CharField(max_length=255, null=True, blank=True)
    #-----------------PROCEDENCIA-----------------------
    establecimiento = models.CharField(max_length=255, default='')
    direccion_procedencia = models.CharField(max_length=255, default='ZONA RURAL')
    localidad_procedencia = models.CharField(max_length=255, choices=LOCALIDADES, null=True, blank=True)
    provincia_procedencia = models.CharField(max_length=255, choices=PROVINCIAS, null=True, blank=True)
    kilometros = models.CharField(max_length=255, null=True, blank=True)
    tarifa = models.CharField(max_length=255, null=True, blank=True)
    tarifa_referencia = models.CharField(max_length=255, null=True, blank=True)
    declaracion_juarada_nombre = models.CharField(max_length=255, null=True, blank=True)
    declaracion_juarada_dni = models.CharField(max_length=255, null=True, blank=True)
    docfile = models.FileField(upload_to='cp_nuevas', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.numero
    #funcion para devolver el nombre de usuario que se agrega al serializer
    def nombreUser(self):
        return self.user.nombre
    
    def nombreChofer(self):
        return self.chofer.nombre
    
    def localidadDestino(self):
        return self.destino.localidad

class CartaDePorteDescargada(models.Model):
    cp = models.ForeignKey(CartaDePorte, on_delete=models.CASCADE)
    contrato = models.ForeignKey(ContratoMercaderia, on_delete=models.CASCADE, null=True, blank=True)
    kilos_descargados = models.IntegerField(null=True, blank=True)
    kilos_merma = models.IntegerField(blank=True, default=0)    
    observaciones_descarga = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def kgs_finales(self):
        if self.kilos_merma == None:
            self.kilos_merma = 0
        if self.kilos_descargados == None:
            self.kilos_descargados = 0
        kilos_finales = self.kilos_descargados-self.kilos_merma
        return kilos_finales
    
    @property
    @admin.display
    def cosecha_display_admin(self):
        return self.cp.cosecha

    class Meta: 
        app_label = 'mercaderias'
        managed = True
   
    def __str__(self):
        return self.cp.numero
        
class FijacionContrato(models.Model): 
    fecha = models.DateField()
    contrato = models.ForeignKey(ContratoMercaderia, on_delete=models.CASCADE)
    kilos_fijados = models.BigIntegerField()
    precio = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   

    class Meta: 
        app_label = 'mercaderias'
   
    def __str__(self):
        return self.pk

class PesificacionContrato(models.Model): 
    fecha = models.DateField()
    contrato = models.ForeignKey(ContratoMercaderia, on_delete=models.CASCADE)
    kilos_pesificados = models.BigIntegerField()
    tipo_de_cambio = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_cambio(self):
        tot = self.contrato.precio*(self.kilos_pesificados/1000)*self.tipo_de_cambio
        return tot

    class Meta: 
        app_label = 'mercaderias'
   
    def __str__(self):
        return self.pk

class PlanSiembra(models.Model):     
    superficie_sembrada = models.IntegerField()
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)
    cultivo = models.CharField(max_length=20, choices=PRODUCTO_TYPE, default=SOJA)
    variedad = models.CharField(max_length=255)
    descripcion = models.TextField(max_length=600)
    campania = models.CharField(max_length=60, choices=COSECHAS)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    titular = models.ForeignKey(EmpresaRepresentada, on_delete=models.CASCADE, null=True, blank=True)
    class Meta: 
        app_label = 'mercaderias'
        managed = True

    def __str__(self):
        return self.campo.nombre

class OrdenDeLabor(models.Model):
    fecha = models.DateField()
    titular = models.ForeignKey(EmpresaRepresentada, on_delete=models.CASCADE, null=True, blank=True)
    cultivo = models.CharField(max_length=20, choices=PRODUCTO_TYPE, default=SOJA)
    contratista = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    campania = models.CharField(max_length=60, choices=COSECHAS)
    labor = models.CharField(max_length=60)
    tipo_labor = models.CharField(max_length=60)
    campo = models.ManyToManyField(Campo, blank=True)   
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_has(self):
        total_has = sum([obj.hectareas for obj in self.campo.all()])
        return total_has
    
    @property
    def total_ismo(self):
        total_i_utilizados = []
        for obj in self.item.all():
            d = dict(producto=obj.insumo, total=obj.dosis*self.total_has)
            total_i_utilizados.append(d)
        return total_i_utilizados

    class Meta: 
        app_label = 'mercaderias'
        managed = True

    def __str__(self):
        return f'{self.pk}'

class ItemLabor(models.Model):
    insumo = models.ForeignKey(Articulo, on_delete=models.CASCADE, null=True, blank=True)
    dosis = models.FloatField(null=True, blank=True)
    orden = models.ForeignKey(OrdenDeLabor, related_name='item', on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        app_label = 'mercaderias'
        managed = True

    def __str__(self):
        return self.orden.labor

class Lote(models.Model):
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)
    hectareas = models.FloatField()
    propietario = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.propietario} - {self.campo} - {self.hectareas}'

    class Meta: 
        app_label = 'mercaderias'
        managed = True
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'

class Arrendamiento(models.Model):
    empresa = models.ForeignKey(EmpresaRepresentada, on_delete=models.CASCADE)
    arrendador = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    toneladas_x_ha = models.FloatField(null=True, blank=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def tt_totales(self):
        return round(float(self.toneladas_x_ha*self.lote.hectareas),2)

    class Meta: 
        app_label = 'mercaderias'
        managed = True
        verbose_name = 'Contrato de Arrendamiento'
        verbose_name_plural = 'Arrendamientos'