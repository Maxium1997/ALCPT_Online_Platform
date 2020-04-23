from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.generic import TemplateView

from ALCPT_Online_Platform.settings import LOGOUT_REDIRECT_URL

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


def logout(request):
    auth.logout(request)
    return redirect(LOGOUT_REDIRECT_URL)