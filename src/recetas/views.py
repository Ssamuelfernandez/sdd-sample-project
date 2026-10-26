from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView

from .forms import RecetaForm
from .models import Receta


class RecetaListView(ListView):
    context_object_name = 'recetas'
    queryset = Receta.objects.filter(publicada=True)


class RecetaDetailView(DetailView):
    model = Receta

    def get_queryset(self):
        # Los borradores solo los ve el admin; para el resto no existen (404).
        if self.request.user.is_staff:
            return Receta.objects.all()
        return Receta.objects.filter(publicada=True)


class RecetaCreateView(CreateView):
    model = Receta
    form_class = RecetaForm

    def form_valid(self, form):
        # Tras guardar redirige a get_absolute_url(); así recargar no duplica la receta (CL-15).
        respuesta = super().form_valid(form)
        if not self.object.publicada:
            messages.success(self.request, 'Receta guardada como borrador. Aparecerá en la portada cuando se publique.')
            if not self.request.user.is_staff:
                return redirect('recetas:inicio')
        return respuesta


@method_decorator(staff_member_required, name='dispatch')
class BorradoresListView(ListView):
    context_object_name = 'recetas'
    template_name = 'recetas/borradores.html'
    queryset = Receta.objects.filter(publicada=False)


@staff_member_required
@require_POST
def cambiar_publicacion(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    receta.publicada = not receta.publicada
    if receta.publicada:
        # Al publicar un borrador pasa a ser la receta más reciente de la portada.
        receta.fecha_publicacion = timezone.now()
        messages.success(request, f'«{receta.titulo}» se ha publicado.')
    else:
        messages.success(request, f'«{receta.titulo}» ha pasado a borradores.')
    receta.save(update_fields=['publicada', 'fecha_publicacion'])

    siguiente = request.POST.get('siguiente')
    if siguiente and url_has_allowed_host_and_scheme(siguiente, allowed_hosts={request.get_host()}):
        return redirect(siguiente)
    return redirect(receta)
