from datetime import datetime
from zoneinfo import ZoneInfo

from django.shortcuts import render

MADRID = ZoneInfo('Europe/Madrid')

# Datos de prueba mientras no existe el modelo Receta.
RECETAS_MOCK = [
    {
        'id': 3,
        'titulo': 'Tortilla de patatas',
        'autor': 'Ana',
        'descripcion': 'La clásica, jugosa por dentro y con cebolla.',
        'fecha_publicacion': datetime(2026, 10, 23, 18, 30, tzinfo=MADRID),
    },
    {
        'id': 2,
        'titulo': 'Pasta al pesto',
        'autor': 'Luis',
        'descripcion': 'Albahaca fresca, piñones y parmesano en diez minutos.',
        'fecha_publicacion': datetime(2026, 10, 22, 13, 15, tzinfo=MADRID),
    },
    {
        'id': 1,
        'titulo': 'Gazpacho andaluz',
        'autor': 'Carmen',
        'descripcion': '',
        'fecha_publicacion': datetime(2026, 10, 20, 11, 0, tzinfo=MADRID),
    },
]


def inicio(request):
    # ?vacio=1 permite ver el estado vacío mientras se usan datos de prueba.
    recetas = [] if request.GET.get('vacio') else RECETAS_MOCK
    return render(request, 'recetas/receta_list.html', {'recetas': recetas})
