from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from registration.models import Student

from registration.models import Student
from registration.forms import StudentProfileUpdateForm, SchoolForm, CollegeForm


@login_required
def studentProfile(request):
    try:
        context = {'student': request.user.student}
        return render(request, 'student/profile.html', context)
    except ObjectDoesNotExist:
        return redirect(request.META.get('HTTP_REFERER'))


@method_decorator(login_required, name='dispatch')
class StudentProfileUpdateView(UpdateView):
    model = Student
    template_name = 'student/profile.html'
    form_class = SchoolForm
    second_form_class = CollegeForm
    success_url = 'profile'

    def get_context_data(self, **kwargs):
        context = super(StudentProfileUpdateView, self).get_context_data(**kwargs)
        context['school_form'] = self.form_class
        context['college_form'] = self.second_form_class(super(StudentProfileUpdateView, self).form_class)
        return context

    # def get_form(self, form_class=None):



    def get_object(self, queryset=None):
        return Student.objects.get(pk=self.request.user.student.id)

