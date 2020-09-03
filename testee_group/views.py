from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import View

from registration.models import User
from registration.definition import Privilege

# Create your views here.


@method_decorator(login_required, name='dispatch')
class TesteeGroupListView(View):
    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.TBManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(TesteeGroupListView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        template = 'question/TBManager_index.html'
        context = {'questions': Question.objects.all(),
                   'question_filter_form': QuestionFilterForm()}
        return render(request, template, context)