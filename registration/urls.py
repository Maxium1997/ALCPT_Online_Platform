from django.urls import path, include
from django.contrib.auth.views import LoginView

from registration.views import IndexView, SignUpView, ProfileEditView
from registration.views import logout, profile


urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', logout, name='logout'),

    path('accounts/', include([
        path('signup', SignUpView.as_view(), name='sign_up'),
        path('profile', profile, name='profile'),
        path('edit', ProfileEditView.as_view(), name='profile_edit'),
    ])),
]
