from django.urls import path, include

from alcpt.views import IndexView
from registration.views.user import UserListView, UserDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('SystemManager/', include([
        path('user/', include([
            path('list', UserListView.as_view(), name='user_list'),
            path('<pk>/view', UserDetailView.as_view(), name='view_user_detail'),
        ])),

        path('', include('unit.urls')),
    ])),

    path('TestManager/', include([
        path('', include('testee_group.urls')),
    ])),

    path('TBOperator/', include([
        path('', include('question.tbo_urls'))
    ])),

    path('TBManager/', include([
        path('', include('question.tbm_urls'))
    ]))
]
