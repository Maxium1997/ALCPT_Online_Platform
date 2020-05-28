from django.urls import path, include

from question.views import TBOperatorQuestionListView
from question.views import QuestionCreation, ListeningQuestionCreateView, ReadingQuestionCreateView


urlpatterns = [
    path('question/', include([
        path('list', TBOperatorQuestionListView.as_view(), name='TBOperator_question_list'),
        path('creation/', include([
            path('',  QuestionCreation.as_view(), name='question_creation'),
            path('listening', ListeningQuestionCreateView.as_view(), name='listening_question_creation'),
            path('reading', ReadingQuestionCreateView.as_view(), name='reading_question_creation'),
        ])),
    ])),
]
