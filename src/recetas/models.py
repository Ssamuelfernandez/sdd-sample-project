from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinLengthValidator
from django.db import models
from django.templatetags.static import static
from django.urls import reverse

IMAGEN_MAX_BYTES = 2 * 1024 * 1024
# Se muestra cuando la receta no tiene foto propia (CA-31).
IMAGEN_GENERICA = 'img/recetas/generica.jpg'


def validar_tamano_imagen(imagen):
    if imagen.size > IMAGEN_MAX_BYTES:
        raise ValidationError('La foto puede pesar como máximo 2 MB.')


class Receta(models.Model):
    titulo = models.CharField('título', max_length=100, validators=[MinLengthValidator(3)])
    autor = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    descripcion = models.CharField('descripción', max_length=300, blank=True)
    # max_length en un TextField solo lo comprueba el formulario, no la base de datos.
    ingredientes = models.TextField(max_length=3000)
    pasos = models.TextField(max_length=5000)
    imagen = models.ImageField(
        upload_to='recetas/',
        blank=True,
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']),
            validar_tamano_imagen,
        ],
    )
    # Sin marcar, la receta es un borrador: no sale en la portada hasta que el admin la publique.
    publicada = models.BooleanField(default=True)
    fecha_publicacion = models.DateTimeField('fecha de publicación', auto_now_add=True)

    class Meta:
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('recetas:detalle', kwargs={'pk': self.pk})

    @property
    def url_imagen(self):
        return self.imagen.url if self.imagen else static(IMAGEN_GENERICA)

    @staticmethod
    def _lineas(texto):
        # Una línea por elemento, ignorando las vacías y los espacios sobrantes.
        return [linea.strip() for linea in texto.splitlines() if linea.strip()]

    def lista_ingredientes(self):
        return self._lineas(self.ingredientes)

    def lista_pasos(self):
        return self._lineas(self.pasos)
