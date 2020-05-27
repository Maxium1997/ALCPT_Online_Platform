from django.urls import path, include

from registration.views.user import UserListView, UserDetailView

urlpatterns = [
    path('SytemManager/', include([
        path('user/', include([
            path('list', UserListView.as_view(), name='user_list'),
            path('<pk>/view', UserDetailView.as_view(), name='view_user_detail'),
        ])),

        path('', include('unit.urls')),
    ])),

    path('TBOperator/', include([
        path('', include('question.urls')),
    ])),
]
