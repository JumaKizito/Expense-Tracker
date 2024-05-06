from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('register/', accounts_views.register, name='register'),
]
