from django.urls import path

from . import api

app_name = 'api'

urlpatterns = [
    path('recetas/', api.RecetaListCreateAPIView.as_view(), name='lista'),
    path('recetas/<int:pk>/', api.RecetaRetrieveAPIView.as_view(), name='detalle'),
]
