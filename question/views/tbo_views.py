from datetime import datetime

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, ListView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from alcpt.decorators import permission_check
from registration.definition import Privilege
from question.models import Question, Choice
from question.definition import QuestionType, State
from question.forms import ListeningQuestionForm, ReadingQuestionForm, ChoiceForm
from question.forms import ListeningQuestionEditForm

# Create your views here.


@method_decorator(login_required, name='dispatch')
class TBOperatorQuestionListView(ListView):
    model = Question
    template_name = 'question/TBOperator_index.html'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.TBOperator
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(TBOperatorQuestionListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        queries = Q(state=State.Passed.value[0]) | Q(state=State.Pending.value[0]) | Q(state=State.Handled.value[0])
        context['questions'] = Question.objects.exclude(queries)
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


@method_decorator(login_required, name='dispatch')
class ReadingQuestionCreateView(View):
    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.TBOperator
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(ReadingQuestionCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        question_form = ReadingQuestionForm(instance=Question())
        choice_forms = [ChoiceForm(prefix=str(x), instance=Choice()) for x in range(4)]
        template = 'question/reading_question_creation.html'
        context = {'question_form': question_form,
                   'choice_forms': choice_forms}
        return render(request, template, context)

    def post(self, request):
        question_form = ReadingQuestionForm(request.POST, instance=Question())
        choice_forms = [ChoiceForm(request.POST, prefix=str(x), instance=Choice()) for x in range(0, 4)]

        if question_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_question = question_form.save(commit=False)
            new_question.created_by = request.user
            new_question.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.source = new_question
                new_choice.save()
            return redirect('TBOperator_question_list')

        context = {'question_form': question_form,
                   'choice_forms': choice_forms}
        template = 'question/reading_question_creation.html'
        return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class QuestionEditView(View):
    QuestionTypeDict = {QuestionType.QA.value[0]: QuestionType.QA.value[1],
                        QuestionType.ShortConversation.value[0]: QuestionType.ShortConversation.value[1],
                        QuestionType.Grammar.value[0]: QuestionType.Grammar.value[1],
                        QuestionType.Phrase.value[0]: QuestionType.Phrase.value[1],
                        QuestionType.ParagraphUnderstanding.value[0]: QuestionType.ParagraphUnderstanding.value[1]}

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.TBOperator
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(QuestionEditView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)

        if question.state == State.Saved.value[0] or question.state == State.Rejected.value[0]:
            pass
        else:
            messages.warning(request, "Get Failed, question state is not Saved or Rejected")
            return redirect(request.META.get('HTTP_REFERER'))

        if self.QuestionTypeDict[question.q_type] == 'Listening':
            question_form = ListeningQuestionEditForm(instance=question)
        elif self.QuestionTypeDict[question.q_type] == 'Reading':
            question_form = ReadingQuestionForm(instance=question)
        else:
            messages.error(request, "Unknown question type")
            return redirect(request.META.get('HTTP_REFERER'))

        choices = question.choice_set.all()
        choice_forms = [ChoiceForm(prefix=str(choice.id), instance=choice) for choice in choices]
        template = 'question/edit.html'

        context = {'question': question,
                   'question_form': question_form,
                   'choice_forms': choice_forms}

        return render(request, template, context)

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)

        if self.QuestionTypeDict[question.q_type] == 'Listening':
            question_form = ListeningQuestionEditForm(request.POST, instance=question)
        elif self.QuestionTypeDict[question.q_type] == 'Reading':
            question_form = ReadingQuestionForm(request.POST, instance=question)
        else:
            messages.error(request, "Unknown question type")
            return redirect(request.META.get('HTTP_REFERER'))

        choices = question.choice_set.all()
        choice_forms = [ChoiceForm(request.POST, prefix=str(choice.id), instance=choice) for choice in choices]

        if question_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            question = question_form.save(commit=False)
            question.state = State.Saved.value[0]
            question.updated_by = request.user
            question.save()
            for cf in choice_forms:
                choice = cf.save(commit=False)
                choice.source = question
                choice.save()
            messages.success(request, "Updated Successfully, question state became Saved")
        return redirect('TBOperator_question_list')


@permission_check(Privilege.TBOperator)
def question_submit(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if question.state is State.Saved.value[0]:
        question.state = State.Pending.value[0]
        question.save()
        messages.success(request, "Successfully Submitted")
    else:
        messages.warning(request, "Failed Pass. The state of question is not saved.")

    return redirect('TBOperator_question_list')


@permission_check(Privilege.TBOperator)
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if question.state is State.Saved.value[0]:
        question.delete()
        messages.success(request, "Successfully Deleted")
    else:
        messages.warning(request, "Failed Delete. The state of question is not saved.")

    return redirect('TBOperator_question_list')
