from django.urls import path, include

from question.views import QuestionCreation, ListeningQuestionCreateView


urlpatterns = [
    path('question/', include([
        path('creation/', include([
            path('',  QuestionCreation.as_view(), name='question_creation'),
            path('listening', ListeningQuestionCreateView.as_view(), name='listening_question_creation'),
            # path('reading', , name='reading_question_creation'),
        ])),
    ])),
]
