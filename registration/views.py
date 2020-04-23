from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView

from ALCPT_Online_Platform.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from registration.models import User
from registration.forms import SignUpForm

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'sign_up.html'

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('index')


@login_required
def logout(request):
    auth.logout(request)
    return redirect(LOGOUT_REDIRECT_URL)
