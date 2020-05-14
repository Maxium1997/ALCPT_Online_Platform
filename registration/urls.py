from django.urls import path, include
from django.contrib.auth.views import LoginView

from registration.views.user import IndexView, SignUpView, ProfileEditView
from registration.views.user import logout, profile, photo_upload, current_photo_delete
from registration.views.student import StudentProfileUpdateView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', logout, name='logout'),

    path('accounts/', include([
        path('signup', SignUpView.as_view(), name='sign_up'),
        path('profile', profile, name='profile'),
        path('edit', ProfileEditView.as_view(), name='profile_edit'),
    ])),

    path('photo/', include([
        path('upload', photo_upload, name='photo_upload'),
        path('delete/current', current_photo_delete, name='current_photo_delete'),
        # path('delete', photo_delete, name='photo_delete'),
    ])),

    path('student/', include([
        path('profile', StudentProfileUpdateView.as_view(), name='student_profile'),
    ]))
]
