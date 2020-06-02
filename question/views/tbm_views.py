from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, ListView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from alcpt.decorators import permission_check
from registration.definition import Privilege
from question.models import Question
from question.definition import State
from question.forms import RejectReasonForm


@method_decorator(login_required, name='dispatch')
class TBManagerQuestionListView(ListView):
    model = Question
    template_name = 'question/TBManager_index.html'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.TBManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(TBManagerQuestionListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.exclude(state=State.Saved.value[0])
        return context


@method_decorator(login_required, name='dispatch')
class TBManagerReviewListView(ListView):
    model = Question
    template_name = 'question/review.html'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.TBManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(TBManagerReviewListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(state=State.Pending.value[0])
        return context


@permission_check(Privilege.TBManager)
def question_pass(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if question.state is State.Pending.value[0]:
        question.state = State.Passed.value[0]
        question.save()
        messages.success(request, "Successfully Passed")
    else:
        messages.warning(request, "Failed Pass. The state of question is not pending.")

    return redirect('TBManager_review_list')


@permission_check(Privilege.TBManager)
def question_reject(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if question.state is State.Pending.value[0]:
        if request.method == 'POST':

            if question.faulty_reason is None:
                question.faulty_reason = request.POST.get('faulty_reason') + '\n'
            else:
                question.faulty_reason += request.POST.get('faulty_reason') + '\n'

            question.state = State.Rejected.value[0]
            question.save()
            messages.success(request, "Successfully Reject.")
            return redirect('TBManager_review_list')
        else:
            context = {'question': question,
                       'reject_reason_form': RejectReasonForm}
            template = 'question/reject.html'
            return render(request, template, context)
    else:
        messages.warning(request, "Failed Reject. The state of question is not pending.")
        return redirect('TBManager_review_list')


