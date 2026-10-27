from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.authtoken.models import Token

from .models import Receta

DATOS_API = {
    'titulo': 'Tortilla de patatas',
    'autor': 'Ana',
    'ingredientes': 'Huevos\nPatatas',
    'pasos': 'Freír\nCuajar',
}


def crear_receta(titulo, publicada=True, dias_atras=0):
    receta = Receta.objects.create(
        titulo=titulo, autor='Ana', ingredientes='Sal', pasos='Cocinar', publicada=publicada,
    )
    # auto_now_add impide fijar la fecha al crear; se cambia después con update().
    Receta.objects.filter(pk=receta.pk).update(fecha_publicacion=timezone.now() - timedelta(days=dias_atras))
    return receta


class APITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # La migración de datos crea 9 recetas de prueba; aquí se parte de una base vacía.
        Receta.objects.all().delete()
        cls.admin = User.objects.create_user('admin', password='x', is_staff=True, is_superuser=True)
        cls.normal = User.objects.create_user('lector', password='x')
        cls.token_admin = Token.objects.create(user=cls.admin)
        cls.token_normal = Token.objects.create(user=cls.normal)
        cls.lista = reverse('api:lista')

    def post(self, datos, token=None):
        extra = {'HTTP_AUTHORIZATION': f'Token {token.key}'} if token else {}
        return self.client.post(self.lista, datos, content_type='application/json', **extra)


class LecturaAPITests(APITestCase):
    def test_listado_solo_publicadas_ordenadas(self):
        crear_receta('Antigua', dias_atras=2)
        crear_receta('Reciente', dias_atras=0)
        crear_receta('Oculta', publicada=False)
        respuesta = self.client.get(self.lista)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual([r['titulo'] for r in respuesta.json()], ['Reciente', 'Antigua'])

    def test_campos_de_la_respuesta(self):
        receta = crear_receta('Pasta')
        datos = self.client.get(reverse('api:detalle', kwargs={'pk': receta.pk})).json()
        self.assertEqual(
            datos,
            {
                'id': receta.pk, 'titulo': 'Pasta', 'autor': 'Ana', 'descripcion': '',
                'ingredientes': 'Sal', 'pasos': 'Cocinar', 'estado': 'publicada',
            },
        )

    def test_detalle_de_borrador_o_inexistente_404(self):
        borrador = crear_receta('Oculta', publicada=False)
        self.assertEqual(self.client.get(reverse('api:detalle', kwargs={'pk': borrador.pk})).status_code, 404)
        self.assertEqual(self.client.get(reverse('api:detalle', kwargs={'pk': 9999})).status_code, 404)
        self.assertEqual(self.client.get('/api/recetas/abc/').status_code, 404)

    def test_el_admin_con_token_tampoco_ve_borradores(self):
        borrador = crear_receta('Oculta', publicada=False)
        cabecera = {'HTTP_AUTHORIZATION': f'Token {self.token_admin.key}'}
        self.assertEqual(self.client.get(self.lista, **cabecera).json(), [])
        respuesta = self.client.get(reverse('api:detalle', kwargs={'pk': borrador.pk}), **cabecera)
        self.assertEqual(respuesta.status_code, 404)


class CreacionAPITests(APITestCase):
    def test_post_admin_crea_borrador(self):
        respuesta = self.post(DATOS_API, self.token_admin)
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(respuesta.json()['estado'], 'borrador')
        self.assertEqual(Receta.objects.count(), 1)
        receta = Receta.objects.get()
        self.assertFalse(receta.publicada)
        self.assertFalse(receta.imagen)
        self.assertIsNotNone(receta.fecha_publicacion)

    def test_post_ignora_publicada_y_estado(self):
        for extra in ({'publicada': True}, {'estado': 'publicada'}, {'publicada': True, 'estado': 'publicada'}):
            respuesta = self.post({**DATOS_API, **extra}, self.token_admin)
            self.assertEqual(respuesta.status_code, 201)
            self.assertEqual(respuesta.json()['estado'], 'borrador')
        self.assertFalse(Receta.objects.filter(publicada=True).exists())

    def test_borrador_no_es_visible_en_publico(self):
        self.post(DATOS_API, self.token_admin)
        pk = Receta.objects.get().pk
        self.assertEqual(self.client.get(self.lista).json(), [])
        self.assertNotContains(self.client.get(reverse('recetas:inicio')), 'Tortilla de patatas')
        self.assertEqual(self.client.get(reverse('recetas:detalle', kwargs={'pk': pk})).status_code, 404)

    def test_borrador_aparece_en_borradores_del_admin(self):
        self.post(DATOS_API, self.token_admin)
        self.client.force_login(self.admin)
        self.assertContains(self.client.get(reverse('recetas:borradores')), 'Tortilla de patatas')

    def test_post_sin_token_401(self):
        self.assertEqual(self.post(DATOS_API).status_code, 401)
        self.assertEqual(Receta.objects.count(), 0)

    def test_post_con_token_inventado_401(self):
        respuesta = self.client.post(
            self.lista, DATOS_API, content_type='application/json', HTTP_AUTHORIZATION='Token inventado'
        )
        self.assertEqual(respuesta.status_code, 401)
        self.assertEqual(Receta.objects.count(), 0)

    def test_post_con_sesion_de_admin_sin_token_401(self):
        # La API solo acepta token: una sesión del admin no basta.
        self.client.force_login(self.admin)
        self.assertEqual(self.post(DATOS_API).status_code, 401)
        self.assertEqual(Receta.objects.count(), 0)

    def test_post_no_admin_403(self):
        self.assertEqual(self.post(DATOS_API, self.token_normal).status_code, 403)
        self.assertEqual(Receta.objects.count(), 0)

    def test_metodos_no_permitidos(self):
        receta = crear_receta('Pasta')
        url = reverse('api:detalle', kwargs={'pk': receta.pk})
        cabecera = {'HTTP_AUTHORIZATION': f'Token {self.token_admin.key}'}
        for metodo in (self.client.put, self.client.patch, self.client.delete):
            respuesta = metodo(url, DATOS_API, content_type='application/json', **cabecera)
            self.assertEqual(respuesta.status_code, 405)
        receta.refresh_from_db()
        self.assertEqual(receta.titulo, 'Pasta')


class ValidacionAPITests(APITestCase):
    def test_campos_obligatorios(self):
        for campo in ('titulo', 'autor', 'ingredientes', 'pasos'):
            datos = {k: v for k, v in DATOS_API.items() if k != campo}
            respuesta = self.post(datos, self.token_admin)
            self.assertEqual(respuesta.status_code, 400, campo)
            self.assertIn(campo, respuesta.json())
        self.assertEqual(Receta.objects.count(), 0)

    def test_solo_espacios_es_invalido(self):
        for campo in ('titulo', 'autor', 'ingredientes', 'pasos'):
            respuesta = self.post({**DATOS_API, campo: '  \n '}, self.token_admin)
            self.assertEqual(respuesta.status_code, 400, campo)
        self.assertEqual(Receta.objects.count(), 0)

    def test_longitudes_limite(self):
        casos = [
            ('titulo', 3, 100), ('autor', 2, 50), ('descripcion', 0, 300),
            ('ingredientes', 1, 3000), ('pasos', 1, 5000),
        ]
        for campo, minimo, maximo in casos:
            validos = ['a' * maximo] + (['a' * minimo] if minimo > 1 else [])
            invalidos = ['a' * (maximo + 1)] + (['a' * (minimo - 1)] if minimo > 1 else [])
            for texto in validos:
                self.assertEqual(self.post({**DATOS_API, campo: texto}, self.token_admin).status_code, 201, campo)
            for texto in invalidos:
                self.assertEqual(self.post({**DATOS_API, campo: texto}, self.token_admin).status_code, 400, campo)

    def test_descripcion_opcional(self):
        respuesta = self.post({**DATOS_API, 'descripcion': 'Clásica'}, self.token_admin)
        self.assertEqual(respuesta.json()['descripcion'], 'Clásica')

    def test_html_se_devuelve_como_texto(self):
        respuesta = self.post({**DATOS_API, 'titulo': '<script>alert(1)</script>'}, self.token_admin)
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(respuesta.json()['titulo'], '<script>alert(1)</script>')
        self.assertEqual(respuesta['Content-Type'], 'application/json')


class RegresionWebTests(APITestCase):
    def test_la_web_sigue_igual(self):
        receta = crear_receta('Pasta')
        self.post(DATOS_API, self.token_admin)
        self.assertContains(self.client.get(reverse('recetas:inicio')), 'Pasta')
        self.assertEqual(self.client.get(receta.get_absolute_url()).status_code, 200)
        self.assertEqual(self.client.get(reverse('recetas:nueva')).status_code, 200)
        self.assertEqual(self.client.get('/admin/').status_code, 302)
        self.assertEqual(Receta.objects.count(), 2)
