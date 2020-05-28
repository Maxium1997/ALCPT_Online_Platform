from django.urls import path, include

from question.views.tbm_views import TBManagerQuestionListView, TBManagerReviewListView
from question.views.tbm_views import question_pass


urlpatterns = [
    path('question/', include([
        path('list', TBManagerQuestionListView.as_view(), name='TBManager_question_list'),
        path('review', TBManagerReviewListView.as_view(), name='TBManager_review_list'),
        path('<pk>/', include([
            path('pass', question_pass, name='question_pass'),
        ]))
    ])),
]
