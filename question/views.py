from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from registration.definition import Privilege
from question.models import Question, Choice
from question.forms import ListeningQuestionForm, ChoiceForm

# Create your views here.


@method_decorator(login_required, name='dispatch')
class TBOperatorQuestionListView(ListView):
    model = Question
    template_name = 'question/TBOperator_index.html'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.SystemManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(TBOperatorQuestionListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.all()
        return context


@method_decorator(login_required, name='dispatch')
class QuestionCreation(TemplateView):
    template_name = 'question/creation.html'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.TBOperator
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(QuestionCreation, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ListeningQuestionCreateView(View):
    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.TBOperator
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(ListeningQuestionCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        question_form = ListeningQuestionForm(instance=Question())
        choice_forms = [ChoiceForm(prefix=str(x), instance=Choice()) for x in range(4)]
        template = 'question/listening_question_creation.html'
        context = {'question_form': question_form,
                   'choice_forms': choice_forms}
        return render(request, template, context)

    def post(self, request):
        question_form = ListeningQuestionForm(request.POST, request.FILES, instance=Question())
        choice_forms = [ChoiceForm(request.POST, prefix=str(x), instance=Choice()) for x in range(0, 4)]

        if question_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_question = question_form.save(commit=False)
            new_question.created_by = request.user
            new_question.q_file.save("Question{}.mp3".format(datetime.now().strftime("%Y-%m-%d %H.%M.%S")),
                                     request.FILES.get('q_file'),
                                     save=False)
            new_question.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.source = new_question
                new_choice.save()
            return redirect('TBOperator_question_list')

        context = {'question_form': question_form,
                   'choice_forms': choice_forms}
        template = 'question/listening_question_creation.html'
        return render(request, template, context)

