from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from registration.definition import Privilege
from unit.models import School, College, Department, Squadron


@method_decorator(login_required, name='dispatch')
class UnitListView(ListView):
    model = School
    template_name = 'SystemManager/unit/list.html'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.SystemManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(UnitListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schools'] = School.objects.all()
        context['colleges'] = College.objects.all()
        context['departments'] = Department.objects.all()
        context['squadrons'] = Squadron.objects.all()
        return context
