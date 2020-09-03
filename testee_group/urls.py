from django.urls import path, include

from testee_group.views import TesteeGroupListView

urlpatterns = [
    path('testee_group', include([
        path('list', TesteeGroupListView.as_view(), name='testee_group_list'),
    ])),
]