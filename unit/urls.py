from django.urls import path, include

from unit.views import UnitListView, SchoolCreate, CollegeCreate, DepartmentCreate, SquadronCreate

urlpatterns = [
    path('unit/', include([
        path('list', UnitListView.as_view(), name='unit_list'),
        path('new-school', SchoolCreate.as_view(), name='create_school'),
        path('new-college', CollegeCreate.as_view(), name='create_college'),
        path('new-department', DepartmentCreate.as_view(), name='create_department'),
        path('new-squadron', SquadronCreate.as_view(), name='create_squadron'),
    ]))
]