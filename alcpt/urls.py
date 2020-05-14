from django.urls import path, include

from registration.views.user import UserListView, UserDetailView
from unit.views import UnitListView, SchoolCreate, CollegeCreate, DepartmentCreate, SquadronCreate

urlpatterns = [
    path('SytemManager/', include([
        path('user/', include([
            path('list', UserListView.as_view(), name='user_list'),
            # path('create', UserCreate.as_view(), name='create_user'),
            path('<pk>/view', UserDetailView.as_view(), name='view_user_detail'),
        ])),

        path('unit/', include([
            path('list', UnitListView.as_view(), name='unit_list'),
            path('new-school', SchoolCreate.as_view(), name='create_school'),
            path('new-college', CollegeCreate.as_view(), name='create_college'),
            path('new-department', DepartmentCreate.as_view(), name='create_department'),
            path('new-squadron', SquadronCreate.as_view(), name='create_squadron'),
        ]))
    ])),
]
