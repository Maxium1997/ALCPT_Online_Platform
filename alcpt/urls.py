from django.urls import path, include

from alcpt.views.SystemManager.user import UserListView, UserDetailView
from alcpt.views.SystemManager.unit import UnitListView, SchoolCreate, CollegeCreate

urlpatterns = [
    path('SytemManager/', include([
        path('user/', include([
            path('list', UserListView.as_view(), name='user_list'),
            path('<pk>/view', UserDetailView.as_view(), name='view_user_detail'),
        ])),

        path('unit/', include([
            path('list', UnitListView.as_view(), name='unit_list'),
            path('new-school', SchoolCreate.as_view(), name='create_school'),
            path('new-college', CollegeCreate.as_view(), name='create_college'),
        ]))
    ])),
]
