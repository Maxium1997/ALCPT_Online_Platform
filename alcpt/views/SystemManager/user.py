from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from registration.models import User
from registration.definition import Privilege

# Create your views here.


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'SystemManager/user/list.html'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.SystemManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(UserListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['privilege'] = Privilege.__members__
        return context


@method_decorator(login_required, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'SystemManager/user/detail.html'
    context_object_name = 'user'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.SystemManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)
