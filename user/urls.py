from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout_confirm/', views.LogoutConfirmView.as_view(), name='logout_confirm'),
    path('profile/', views.ProfileDisplay.as_view(), name='profile'),
    path('profile_update', views.ProfileUpdateView.as_view(), name='profile_update'),
]
