from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('confirm/', views.user_confirm),
    path('edit/', views.edit, name='edit'),
    path('upavatar/', views.upavatar, name='upavatar'),
]