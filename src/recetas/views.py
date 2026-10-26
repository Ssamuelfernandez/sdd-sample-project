from django.views.generic import CreateView, DetailView, ListView

from .forms import RecetaForm
from .models import Receta


class RecetaListView(ListView):
    model = Receta
    context_object_name = 'recetas'


class RecetaDetailView(DetailView):
    model = Receta


class RecetaCreateView(CreateView):
    model = Receta
    form_class = RecetaForm
    # Tras guardar redirige a get_absolute_url(); así recargar no duplica la receta (CL-15).
