import io
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import IMAGEN_GENERICA, Receta

MEDIA_PRUEBAS = tempfile.mkdtemp()

DATOS_VALIDOS = {
    'titulo': 'Huevos rotos',
    'autor': 'Ana',
    'descripcion': '',
    'ingredientes': '2 huevos\n\n  Patatas  \n',
    'pasos': 'Fríe las patatas.\nFríe los huevos.',
}


def foto_jpg(nombre='foto.jpg'):
    buffer = io.BytesIO()
    Image.new('RGB', (10, 10), 'orange').save(buffer, 'JPEG')
    return SimpleUploadedFile(nombre, buffer.getvalue(), content_type='image/jpeg')


@override_settings(MEDIA_ROOT=MEDIA_PRUEBAS)
class RecetaTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_PRUEBAS, ignore_errors=True)

    def test_listado_muestra_recetas_de_prueba_de_la_mas_reciente_a_la_mas_antigua(self):
        respuesta = self.client.get(reverse('recetas:inicio'))
        recetas = list(respuesta.context['recetas'])
        self.assertEqual(len(recetas), 9)
        self.assertEqual(recetas[0].titulo, 'Tortilla de patatas')
        self.assertEqual(recetas[-1].titulo, 'Arroz con leche')

    def test_listado_vacio(self):
        Receta.objects.all().delete()
        respuesta = self.client.get(reverse('recetas:inicio'))
        self.assertContains(respuesta, 'Todavía no hay recetas')

    def test_detalle_separa_ingredientes_y_pasos_por_lineas(self):
        receta = Receta.objects.create(**DATOS_VALIDOS)
        self.assertEqual(receta.lista_ingredientes(), ['2 huevos', 'Patatas'])
        respuesta = self.client.get(receta.get_absolute_url())
        self.assertContains(respuesta, '<li>Fríe los huevos.</li>', html=True)

    def test_detalle_inexistente_da_404(self):
        respuesta = self.client.get(reverse('recetas:detalle', kwargs={'pk': 9999}))
        self.assertEqual(respuesta.status_code, 404)

    def test_publicar_sin_foto_usa_la_imagen_generica(self):
        respuesta = self.client.post(reverse('recetas:nueva'), DATOS_VALIDOS)
        receta = Receta.objects.get(titulo='Huevos rotos')
        self.assertRedirects(respuesta, receta.get_absolute_url())
        self.assertFalse(receta.imagen)
        self.assertIn(IMAGEN_GENERICA, receta.url_imagen)

    def test_publicar_con_foto(self):
        self.client.post(reverse('recetas:nueva'), {**DATOS_VALIDOS, 'imagen': foto_jpg()})
        receta = Receta.objects.get(titulo='Huevos rotos')
        self.assertTrue(receta.imagen.name.startswith('recetas/'))
        self.assertEqual(receta.url_imagen, receta.imagen.url)

    def test_rechaza_foto_de_mas_de_2_mb(self):
        foto = foto_jpg()
        grande = SimpleUploadedFile('grande.jpg', foto.read() + b'0' * (2 * 1024 * 1024), content_type='image/jpeg')
        respuesta = self.client.post(reverse('recetas:nueva'), {**DATOS_VALIDOS, 'imagen': grande})
        self.assertContains(respuesta, 'como máximo 2 MB')
        self.assertContains(respuesta, 'Vuelve a adjuntar la foto')
        self.assertFalse(Receta.objects.filter(titulo='Huevos rotos').exists())

    def test_rechaza_texto_renombrado_como_jpg(self):
        falso = SimpleUploadedFile('falso.jpg', b'esto no es una imagen', content_type='image/jpeg')
        respuesta = self.client.post(reverse('recetas:nueva'), {**DATOS_VALIDOS, 'imagen': falso})
        self.assertContains(respuesta, 'no es una imagen válida')

    def test_rechaza_titulo_demasiado_corto(self):
        respuesta = self.client.post(reverse('recetas:nueva'), {**DATOS_VALIDOS, 'titulo': 'Hu'})
        self.assertContains(respuesta, 'al menos 3 caracteres')
