#! /usr/bin/env python3

from django import forms
from .models import *
from django.forms import inlineformset_factory

from django.core.exceptions import ValidationError

class PagoForm(forms.ModelForm): 
    instrumentos = forms.ModelMultipleChoiceField(queryset=InstrumentoPago.objects.none())
    facturas = forms.ModelMultipleChoiceField(queryset=Factura.objects.none())
       
    class Meta:
        model = Pagos
        fields = ['fecha', 'numero', 'proveedor', 'instrumentos', 'facturas']
        widgets = {
            'fecha': forms.DateInput(format=('%d/%m/%Y'),
                attrs={
                    'class':'myDateClass',
                    'placeholder':'Elija una fecha',
                    'id': 'fecha',
                    'name': 'fecha',
            }),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].required = True 
        if 'proveedor' in self.data:
            try:
                prov_id = self.data.get('proveedor')
                self.fields['facturas'].queryset = Factura.objects.filter(proveedor__pk__iexact=prov_id).exclude(estado_pago=True)
                self.fields['instrumentos'].queryset = InstrumentoPago.objects.filter(proveedor__pk__iexact=prov_id).exclude(estado_uilizado=True)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['facturas'].queryset = self.instance.proveedor.factura_set.order_by('fecha').exclude(estado_pago=True)
            self.fields['instrumentos'].queryset = self.instance.proveedor.instrumentopago_set.order_by('instrumento').exclude(estado_uilizado=True)
        
class InstrumentoPagoForm(forms.ModelForm):
    class Meta:
        model = InstrumentoPago
        fields = '__all__'

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
        

    def clean_fecha_vto(self):
        data = self.clean()   
        if data['fecha_vto'] <= data['fecha']:
            raise ValidationError('La fecha de vencimiento debe ser mayor a la de la factura.')
        return data['fecha_vto']
       
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['impuesto'].initial = 21
        self.fields['proveedor'].widget.attrs['class']='col-4 p-2'

'''
class NcForm(forms.ModelForm):
    class Meta:
        model = NotaDeCredito
        fields = '__all__'
    def clean_fecha_vto(self):
        data = self.clean()   
        if data['fecha_vto'] <= data['fecha']:
            raise ValidationError('La fecha de vencimiento debe ser mayor a la de la factura.')
        return data['fecha_vto']
       
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['impuesto'].initial = 21
        self.fields['proveedor'].widget.attrs['class']='col-4 p-2'

class NdForm(forms.ModelForm):
    class Meta:
        model = NotaDeDebito
        fields = '__all__'
    def clean_fecha_vto(self):
        data = self.clean()   
        if data['fecha_vto'] <= data['fecha']:
            raise ValidationError('La fecha de vencimiento debe ser mayor a la de la factura.')
        return data['fecha_vto']
       
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['impuesto'].initial = 21
        self.fields['proveedor'].widget.attrs['class']='col-4 p-2'
'''
        
class ProveedorForm(forms.ModelForm):                 
    class Meta:
        model = Proveedor
        fields = '__all__'

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields= '__all__'

ItemsFormset = inlineformset_factory(Factura, ItemFactura, fields=('articulo','cantidad','precio_unitario' ),extra=1, can_delete=True)

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = EmpresaRepresentada
        fields= '__all__'
        exclude = ['usuario']

