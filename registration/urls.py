from django.urls import path, include
from django.contrib.auth.views import LoginView

from registration.views import IndexView
from registration.views import logout


urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('accounts/', include([
        path('login', LoginView.as_view(template_name='login.html'), name='login'),
        path('logout', logout, name='logout'),
    ]))
]