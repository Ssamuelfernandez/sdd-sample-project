from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.files import File
from django.db import migrations

MADRID = ZoneInfo('Europe/Madrid')
# Las fotos de prueba están en static/ (sí van a Git) y se copian a media/ al migrar.
CARPETA_FOTOS = settings.BASE_DIR / 'static' / 'img' / 'recetas'

RECETAS = [
    {
        'titulo': 'Arroz con leche',
        'autor': 'Pedro',
        'foto': 'arroz-con-leche.jpg',
        'descripcion': 'Con canela y piel de limón, como en Asturias.',
        'ingredientes': (
            '1 litro de leche entera\n'
            '100 g de arroz redondo\n'
            '100 g de azúcar\n'
            '1 rama de canela\n'
            'Piel de 1 limón\n'
            'Canela molida para decorar'
        ),
        'pasos': (
            'Calienta la leche con la canela y la piel de limón.\n'
            'Cuando hierva, añade el arroz y baja el fuego.\n'
            'Cuece unos 40 minutos removiendo a menudo para que no se pegue.\n'
            'Añade el azúcar y cuece 5 minutos más.\n'
            'Retira la canela y el limón, reparte en cuencos y espolvorea canela molida.'
        ),
        'fecha_publicacion': datetime(2026, 10, 10, 19, 0, tzinfo=MADRID),
    },
    {
        'titulo': 'Ensalada César',
        'autor': 'Sara',
        'foto': 'ensalada-cesar.jpg',
        'descripcion': '',
        'ingredientes': (
            '1 lechuga romana\n'
            '2 rebanadas de pan\n'
            '50 g de parmesano en lascas\n'
            '1 yema de huevo\n'
            '2 filetes de anchoa\n'
            '1 diente de ajo\n'
            'Zumo de medio limón\n'
            '100 ml de aceite de oliva'
        ),
        'pasos': (
            'Corta el pan en dados y tuéstalo en una sartén con un poco de aceite.\n'
            'Tritura la yema, las anchoas, el ajo y el limón.\n'
            'Añade el aceite en hilo hasta formar una salsa espesa.\n'
            'Lava y trocea la lechuga.\n'
            'Mezcla la lechuga con la salsa y termina con los picatostes y el parmesano.'
        ),
        'fecha_publicacion': datetime(2026, 10, 12, 13, 30, tzinfo=MADRID),
    },
    {
        'titulo': 'Pollo al curry con arroz basmati',
        'autor': 'Diego',
        'foto': 'pollo-al-curry.jpg',
        'descripcion': 'Cremoso, ligeramente picante y listo en media hora.',
        'ingredientes': (
            '500 g de contramuslo de pollo\n'
            '1 cebolla\n'
            '2 dientes de ajo\n'
            '2 cucharadas de curry en polvo\n'
            '400 ml de leche de coco\n'
            '250 g de arroz basmati\n'
            'Cilantro fresco\n'
            'Aceite y sal'
        ),
        'pasos': (
            'Cuece el arroz basmati según las instrucciones del paquete.\n'
            'Corta el pollo en dados y dóralo en una sartén con aceite.\n'
            'Retira el pollo y sofríe la cebolla y el ajo picados.\n'
            'Añade el curry, remueve un minuto y vierte la leche de coco.\n'
            'Devuelve el pollo a la sartén, cuece 15 minutos y sirve con el arroz y cilantro.'
        ),
        'fecha_publicacion': datetime(2026, 10, 14, 21, 10, tzinfo=MADRID),
    },
    {
        'titulo': 'Bizcocho de yogur',
        'autor': 'Lucía',
        'foto': 'bizcocho-de-yogur.jpg',
        'descripcion': 'El de toda la vida: un vaso de yogur como medida para todo.',
        'ingredientes': (
            '1 yogur natural (el vaso sirve de medida)\n'
            '3 huevos\n'
            '2 vasos de azúcar\n'
            '3 vasos de harina\n'
            '1 vaso de aceite de girasol\n'
            '1 sobre de levadura química\n'
            'Ralladura de 1 limón'
        ),
        'pasos': (
            'Precalienta el horno a 180 °C.\n'
            'Bate los huevos con el azúcar hasta que blanqueen.\n'
            'Añade el yogur, el aceite y la ralladura de limón.\n'
            'Incorpora la harina tamizada con la levadura, sin batir en exceso.\n'
            'Vierte en un molde engrasado y hornea 40 minutos.'
        ),
        'fecha_publicacion': datetime(2026, 10, 16, 17, 20, tzinfo=MADRID),
    },
    {
        'titulo': 'Lentejas de la abuela',
        'autor': 'Javier',
        'foto': 'lentejas.jpg',
        'descripcion': 'Con chorizo, verduras y mucha paciencia a fuego lento.',
        'ingredientes': (
            '400 g de lentejas pardinas\n'
            '1 chorizo\n'
            '1 cebolla\n'
            '1 zanahoria\n'
            '1 pimiento verde\n'
            '2 dientes de ajo\n'
            '1 hoja de laurel\n'
            '1 cucharadita de pimentón dulce\n'
            'Aceite de oliva y sal'
        ),
        'pasos': (
            'Pica la cebolla, la zanahoria, el pimiento y el ajo.\n'
            'Sofríe las verduras en una olla con un poco de aceite.\n'
            'Añade el chorizo en rodajas y el pimentón, y remueve un minuto.\n'
            'Incorpora las lentejas, el laurel y agua hasta cubrir de sobra.\n'
            'Cuece a fuego lento unos 45 minutos y ajusta de sal al final.'
        ),
        'fecha_publicacion': datetime(2026, 10, 18, 14, 0, tzinfo=MADRID),
    },
    {
        'titulo': 'Gazpacho andaluz',
        'autor': 'Carmen',
        'foto': 'gazpacho-andaluz.jpg',
        'descripcion': '',
        'ingredientes': (
            '1 kg de tomates maduros\n'
            '1 pimiento verde\n'
            '1 pepino\n'
            '1 diente de ajo\n'
            '50 g de pan del día anterior\n'
            '80 ml de aceite de oliva virgen extra\n'
            '2 cucharadas de vinagre de Jerez\n'
            'Sal'
        ),
        'pasos': (
            'Lava y trocea los tomates, el pimiento y el pepino.\n'
            'Remoja el pan en un poco de agua.\n'
            'Tritura todas las verduras con el ajo y el pan escurrido.\n'
            'Añade el aceite, el vinagre y la sal y vuelve a triturar.\n'
            'Cuela el gazpacho y déjalo enfriar en la nevera al menos 2 horas.'
        ),
        'fecha_publicacion': datetime(2026, 10, 20, 11, 0, tzinfo=MADRID),
    },
    {
        'titulo': 'Crema de calabaza',
        'autor': 'Marta',
        'foto': 'crema-de-calabaza.jpg',
        'descripcion': 'Suave, otoñal y con un toque de jengibre.',
        'ingredientes': (
            '800 g de calabaza\n'
            '1 cebolla\n'
            '1 zanahoria\n'
            '1 trozo de jengibre fresco\n'
            '700 ml de caldo de verduras\n'
            'Queso feta y pipas de calabaza para decorar\n'
            'Aceite de oliva y sal'
        ),
        'pasos': (
            'Pela y trocea la calabaza, la cebolla y la zanahoria.\n'
            'Sofríe la cebolla con un poco de aceite hasta que esté transparente.\n'
            'Añade la calabaza, la zanahoria y el jengibre rallado y rehoga 5 minutos.\n'
            'Cubre con el caldo y cuece 25 minutos.\n'
            'Tritura hasta obtener una crema fina y sirve con feta y pipas por encima.'
        ),
        'fecha_publicacion': datetime(2026, 10, 21, 20, 45, tzinfo=MADRID),
    },
    {
        'titulo': 'Pasta al pesto',
        'autor': 'Luis',
        'foto': 'pasta-al-pesto.jpg',
        'descripcion': 'Albahaca fresca, piñones y parmesano en diez minutos.',
        'ingredientes': (
            '320 g de linguine\n'
            '50 g de hojas de albahaca fresca\n'
            '30 g de piñones\n'
            '50 g de parmesano rallado\n'
            '1 diente de ajo\n'
            '100 ml de aceite de oliva\n'
            'Sal'
        ),
        'pasos': (
            'Cuece la pasta en agua con sal según el tiempo del paquete.\n'
            'Mientras tanto, tritura la albahaca, los piñones, el ajo y el parmesano.\n'
            'Añade el aceite poco a poco hasta obtener una salsa cremosa.\n'
            'Escurre la pasta reservando un poco del agua de cocción.\n'
            'Mezcla la pasta con el pesto, aligerando con el agua reservada si hace falta.'
        ),
        'fecha_publicacion': datetime(2026, 10, 22, 13, 15, tzinfo=MADRID),
    },
    {
        'titulo': 'Tortilla de patatas',
        'autor': 'Ana',
        'foto': 'tortilla-de-patatas.jpg',
        'descripcion': 'La clásica, jugosa por dentro y con cebolla.',
        'ingredientes': (
            '6 huevos\n'
            '4 patatas medianas\n'
            '1 cebolla\n'
            'Aceite de oliva virgen extra\n'
            'Sal'
        ),
        'pasos': (
            'Pela las patatas y la cebolla y córtalas en láminas finas.\n'
            'Fríelas a fuego medio en abundante aceite durante 20 minutos, hasta que estén tiernas.\n'
            'Escúrrelas bien y mézclalas con los huevos batidos y una pizca de sal.\n'
            'Deja reposar la mezcla 5 minutos.\n'
            'Cuaja la tortilla en una sartén con un poco de aceite, 3 minutos por cada lado.'
        ),
        'fecha_publicacion': datetime(2026, 10, 23, 18, 30, tzinfo=MADRID),
    },
]


def crear_recetas(apps, schema_editor):
    Receta = apps.get_model('recetas', 'Receta')
    for datos in RECETAS:
        datos = dict(datos)
        foto = datos.pop('foto')
        fecha = datos.pop('fecha_publicacion')
        receta = Receta(**datos)
        # Si la foto ya está en media/ (p. ej. al crear la base de datos de los tests) se reutiliza.
        nombre = f'recetas/{foto}'
        if not receta.imagen.storage.exists(nombre):
            with open(CARPETA_FOTOS / foto, 'rb') as f:
                receta.imagen.storage.save(nombre, File(f))
        receta.imagen = nombre
        receta.save()
        # auto_now_add pisa la fecha al crear, así que se fija después.
        Receta.objects.filter(pk=receta.pk).update(fecha_publicacion=fecha)


def borrar_recetas(apps, schema_editor):
    Receta = apps.get_model('recetas', 'Receta')
    for receta in Receta.objects.filter(titulo__in=[r['titulo'] for r in RECETAS]):
        receta.imagen.delete(save=False)
        receta.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_recetas, borrar_recetas),
    ]
