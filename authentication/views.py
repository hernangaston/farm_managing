#! /usr/bin/env python3
from django.shortcuts import render, redirect
from django.template import loader
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.contrib import messages
 


# Create your views here.
class RegistroView(TemplateView):
    template_name = 'form_registro_login.html'
    success_url = reverse_lazy('fyp:index')
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = UserCreationForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(self.success_url)
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            
            return render(request, self.template_name, {'form':form})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'FORMULARIO DE REGISTRO.'
       
        return context

def loginView(request):
    template_name = 'login.html'
    success_url = 'fyp:index'
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
           
            usuario_log = authenticate(username=nombre_usuario, password=pwd)
            
            if usuario_log is not None:
                login(request, usuario_log)

                return redirect(success_url)
            else:
                messages.error(request, 'Usuario no valido')
        else:
            messages.error(request, 'No es valido el formulario')

    form = AuthenticationForm()
    return render(request, template_name, {'form': form})

def close_session(request):
    logout(request)
    request.session.flush()
    return redirect('fyp:index')
