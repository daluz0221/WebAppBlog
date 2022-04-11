from audioop import reverse
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, View

from users.functions import code_generator

from .models import User    
from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm, VerificationForm

# Create your views here.



class UserEstandarRegisterCreateView(FormView):
    
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = "/"

    def form_valid(self, form):
        code = code_generator();
        usuario = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            coderegistro=code
        )

        #Enviar el código al email del user
        asunto = 'Confirmación de email'
        mensaje = 'Para confirmar su email, por favor ingrese el siguiente código: ' + code
        email_remitente = 'daluz0221@gmail.com'
        #
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email']])
        # Redirigir a pantalla de validación

        
        return HttpResponseRedirect(
            reverse_lazy('users:verification', kwargs={'pk': usuario.id})
        )


class LoginUser(FormView):
    
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
    
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        print(user)
       
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)

        
        


class LogoutUser(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse_lazy('users:login')
        )


class UpdatePassword(FormView):

    template_name = "users/update.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
    
        usuario = self.request.user
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        
        return super(UpdatePassword, self).form_valid(form)


class CodeVerificationView(FormView):

    template_name = "users/verification.html"
    form_class = VerificationForm
    success_url = reverse_lazy('users:login')

    def get_form_kwargs(self) :

        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk'],
        })
        
        return kwargs

    def form_valid(self, form):
    
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )

        return super(CodeVerificationView, self).form_valid(form)