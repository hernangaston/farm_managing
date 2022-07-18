#! /usr/bin/env python3

from django import forms
from django.core.exceptions import ValidationError

from django.forms import BaseInlineFormSet
from django.forms import inlineformset_factory


from comprobantes.models import Articulo, EmpresaRepresentada
from .models import *

class CartaDePorteForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
       
    class Meta:
        model = CartaDePorte
        exclude = ['user', 'titular', 'pesada_en_destino', 'kgs_estimados',\
            'declaracion_calidad', 'conforme', 'condicional', \
            'declaracion_juarada_nombre', 'declaracion_juarada_dni', 'tarifa_referencia', \
            'renspa', 'tipo']

class CartaDePorteDescargadaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cp'].queryset = CartaDePorte.objects.all().filter(cosecha__iexact='2021/2022').filter(grano__iexact='MAIZ')
        self.fields['contrato'].queryset = ContratoMercaderia.objects.all().filter(cosecha__iexact='2021/2022').filter(producto__iexact='MAIZ')        
    class Meta:
        model = CartaDePorteDescargada
        fields = '__all__'

class CompradorForm(forms.ModelForm):
    class Meta:
        model = Destinatario
        fields = '__all__'

class ContratoMercaderiaForm(forms.ModelForm):
    class Meta:
        model = ContratoMercaderia
        fields = '__all__'

    def clean_kilos_pactados(self):
        data = self.cleaned_data['kilos_pactados']       
        if 'kilos_pactados' in self.cleaned_data:
            kilos = int(self.cleaned_data['kilos_pactados'])            
            if kilos<1000:
                raise ValidationError("Los kilos del contrato deben ser mayor a 30.000")
        return data

    
class FijacionContratoForm(forms.ModelForm):
    class Meta:
        model = FijacionContrato
        fields = '__all__'

class PesificacionContratoForm(forms.ModelForm):
    class Meta:
        model = PesificacionContrato
        fields = '__all__'

class OrdenDeLaborForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""
        
        emp = kwargs.pop('initial')
       
        super(OrdenDeLaborForm, self).__init__(*args, **kwargs)
        self.fields['campo'].queryset = emp['campos']
            
    
    class Meta:
        model = OrdenDeLabor
        fields = '__all__'
        exclude = ['titular']   

    campo = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple
    )     
    
class ItemLaborForm(forms.ModelForm):
    insumo_select = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['insumo_select'].queryset = Articulo.objects.all()
    
    class Meta:
        model = ItemLabor
        fields = '__all__'

ItemsFormset = inlineformset_factory(OrdenDeLabor,ItemLabor, fields=('insumo','dosis'), extra=5, can_delete=False)

class ContratoArrendamientoForm(forms.ModelForm):
    class Meta:
        model=Arrendamiento
        fields = '__all__'
        exclude = ['empresa']

class CampoForm(forms.ModelForm):
    class Meta:
        model=Campo
        fields = '__all__'

class LoteForm(forms.ModelForm):
    class Meta:
        model=Lote
        fields = '__all__'