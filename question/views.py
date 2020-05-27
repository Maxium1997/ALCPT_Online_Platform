from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from registration.definition import Privilege
from question.models import Question, Choice
from question.forms import ListeningQuestionForm, ChoiceForm

# Create your views here.


@method_decorator(login_required, name='dispatch')
class QuestionCreation(TemplateView):
    template_name = 'question/creation.html'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.TBOperator
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(QuestionCreation, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ListeningQuestionCreateView(CreateView):
    model = Question
    template_name = 'question/listening_question_creation.html'
    form_class = ListeningQuestionForm

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.TBOperator
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(ListeningQuestionCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if 'question_form' not in kwargs:
            kwargs['question_form'] = ListeningQuestionForm()
        if 'choice1_form' not in kwargs:
            kwargs['choice1_form'] = ChoiceForm()
        if 'choice2_form' not in kwargs:
            kwargs['choice2_form'] = ChoiceForm()
        if 'choice3_form' not in kwargs:
            kwargs['choice3_form'] = ChoiceForm()
        if 'choice4_form' not in kwargs:
            kwargs['choice4_form'] = ChoiceForm()

        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    # def post(self, request, *args, **kwargs):
    #     context = {}
    #     if

    def form_valid(self, form):
        new_question = form.save(commit=False)
