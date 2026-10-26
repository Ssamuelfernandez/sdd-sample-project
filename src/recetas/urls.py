from django.urls import path

from . import views

app_name = 'recetas'

urlpatterns = [
    path('', views.RecetaListView.as_view(), name='inicio'),
    path('recetas/nueva/', views.RecetaCreateView.as_view(), name='nueva'),
    path('recetas/borradores/', views.BorradoresListView.as_view(), name='borradores'),
    path('recetas/<int:pk>/', views.RecetaDetailView.as_view(), name='detalle'),
    path('recetas/<int:pk>/publicacion/', views.cambiar_publicacion, name='cambiar_publicacion'),
]
