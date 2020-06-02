from django.urls import path, include

from question.views.tbo_views import TBOperatorQuestionListView
from question.views.tbo_views import QuestionCreation, ListeningQuestionCreateView, ReadingQuestionCreateView
from question.views.tbo_views import QuestionEditView, question_submit, question_delete


urlpatterns = [
    path('question/', include([
        path('list', TBOperatorQuestionListView.as_view(), name='TBOperator_question_list'),
        path('creation/', include([
            path('',  QuestionCreation.as_view(), name='question_creation'),
            path('listening', ListeningQuestionCreateView.as_view(), name='listening_question_creation'),
            path('reading', ReadingQuestionCreateView.as_view(), name='reading_question_creation'),
        ])),
        path('<pk>/', include([
            path('submit', question_submit, name='question_submit'),
            path('edit', QuestionEditView.as_view(), name='question_edit'),
            path('delete', question_delete, name='question_delete'),
        ]))

    ])),
]
