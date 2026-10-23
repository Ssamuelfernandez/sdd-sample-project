from django.urls import path

from . import views

app_name = 'recetas'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('recetas/nueva/', views.nueva, name='nueva'),
    path('recetas/<int:pk>/', views.detalle, name='detalle'),
]
