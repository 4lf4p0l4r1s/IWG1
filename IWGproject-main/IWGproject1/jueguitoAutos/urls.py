from django.urls import path,include
from .views import login_usuario
from . import views
from .views import dashboard
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('registro_usuario/', views.registro_usuario, name='registro_usuario'),
    path('ranking/', views.ranking, name='ranking'),
    path('login/', login_usuario, name='login_usuario'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registrar_kilometraje/', views.registrar_kilometraje, name='registrar_kilometraje'),
]

