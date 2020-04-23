from django.shortcuts import render
from django.views.generic import ListView, DetailView

from registration.models import User
from registration.definition import Privilege

# Create your views here.


class UserListView(ListView):
    model = User
    template_name = 'SystemManager/user/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['privilege'] = Privilege.__members__
        return context


class UserDetailView(DetailView):
    model = User
    template_name = 'SystemManager/user/detail.html'
    context_object_name = 'user'
