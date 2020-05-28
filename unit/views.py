from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.template.defaultfilters import slugify

from registration.definition import Privilege
from unit.models import School, College, Department, Squadron
from unit.forms import SchoolCreateForm, CollegeCreateForm, DepartmentCreateForm, SquadronCreateForm


@method_decorator(login_required, name='dispatch')
class UnitListView(ListView):
    model = School
    template_name = 'unit/list.html'

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
    template_name = 'unit/create_school.html'
    form_class = SchoolCreateForm
    context_object_name = 'school'
    success_url = reverse_lazy('unit_list')

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.SystemManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(SchoolCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        school = form.save(commit=False)
        if School.objects.filter(name=school.name, address=school.address, website=school.website):
            messages.error(self.request, "Failed Created, the school is existed.")
            return redirect(self.request.META.get('HTTP_REFERER'))
        else:
            school.save()
            messages.success(self.request, "Successfully Created.")
        return redirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class CollegeCreate(CreateView):
    model = College
    template_name = 'unit/create_college.html'
    form_class = CollegeCreateForm
    context_object_name = 'college'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.SystemManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(CollegeCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        college = form.save(commit=False)
        if College.objects.filter(school=form.cleaned_data['school'], name=college.name):
            messages.error(self.request, "Failed Created, the college is existed.")
            return redirect(self.request.META.get('HTTP_REFERER'))
        else:
            college.school = form.cleaned_data['school']
            college.save()
            messages.success(self.request, "Successfully Created.")
        return redirect('unit_list')


@method_decorator(login_required, name='dispatch')
class DepartmentCreate(CreateView):
    model = Department
    template_name = 'unit/create_department.html'
    form_class = DepartmentCreateForm
    context_object_name = 'department'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.SystemManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(DepartmentCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        department = form.save(commit=False)
        if Department.objects.filter(college=form.cleaned_data['college'], name=department.name):
            messages.error(self.request, "Failed Created, the department is existed.")
            return redirect(self.request.META.get('HTTP_REFERER'))
        else:
            department.college = form.cleaned_data['college']
            department.save()
            messages.success(self.request, "Successfully Created.")
        return redirect('unit_list')


@method_decorator(login_required, name='dispatch')
class SquadronCreate(CreateView):
    model = Squadron
    template_name = 'unit/create_squadron.html'
    form_class = SquadronCreateForm
    context_object_name = 'squadron'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.SystemManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(SquadronCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        squadron = form.save(commit=False)
        if Squadron.objects.filter(college=form.cleaned_data['college'], name=squadron.name):
            messages.error(self.request, "Failed Created, the squadron is existed.")
            return redirect(self.request.META.get('HTTP_REFERER'))
        else:
            squadron.college = form.cleaned_data['college']
            squadron.save()
            messages.success(self.request, "Successfully Created.")
        return redirect('unit_list')
