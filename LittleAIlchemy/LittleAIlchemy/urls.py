"""LittleAIlchemy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import inicio, MiLoginView

urlpatterns = [
    path('login/', MiLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('signup/', views.registro, name='registro'),
    path('', login_required(inicio), name='inicio'),
    path('alquimia/', views.alquimia, name='alquimia'),
    path('challenge/', views.desafio, name='challenge'),
    path('admin/', admin.site.urls),
]

handler404 = 'LittleAIlchemy.views.custom404'

#urlpatterns = [
#    path('admin/', admin.site.urls),
#]
