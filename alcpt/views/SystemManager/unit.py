from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.template.defaultfilters import slugify

from registration.definition import Privilege
from unit.models import School, College, Department, Squadron
from unit.forms import SchoolCreateForm, CollegeCreateForm


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


@method_decorator(login_required, name='dispatch')
class SchoolCreate(SuccessMessageMixin, CreateView):
    model = School
    template_name = 'SystemManager/unit/create_school.html'
    form_class = SchoolCreateForm
    context_object_name = 'school'
    # Cannot show normally
    success_message = "Create successfully."
    success_url = reverse_lazy('unit_list')

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.SystemManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(SchoolCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class CollegeCreate(CreateView):
    model = College
    template_name = 'SystemManager/unit/create_college.html'
    form_class = CollegeCreateForm
    context_object_name = 'college'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.SystemManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(CollegeCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        college = form.save(commit=False)
        college.school = form.cleaned_data['school']
        college.save()
        return redirect('unit_list')
