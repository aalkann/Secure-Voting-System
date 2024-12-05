from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomAuthenticationForm, CustomUserCreationForm

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "authentication_app/login.html"

class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'authentication_app/register.html'
    success_url = reverse_lazy('authentication_app:login')

class CustomLogoutView(LogoutView):
    template_name = 'authentication_app/login.html'