from django.contrib.auth.views import LogoutView
from django.urls import path

from myproject.accounts import views as v

urlpatterns = [
    path(
        'login/',
        v.MyLoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logged/', v.logged, name='logged')
]
