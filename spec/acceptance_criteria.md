# Criterios de aceptación — Blog de Cocina

Documento basado en los requisitos del [PRD](../PRD.md) y el alcance de [scope.md](scope.md). Cada criterio (CA) indica el requisito (RF/RNF) que valida.

## 1. Criterios por funcionalidad

### 1.1 Publicar receta
- **RF-01 — Acceso al formulario**
  - CA-01: el botón "Nueva receta" aparece en la cabecera de todas las páginas (listado, detalle, formulario y 404).
  - CA-02: al pulsarlo se abre `/recetas/nueva/` con el formulario vacío.
- **RF-02 — Campos de la receta**
  - CA-03: el formulario muestra los campos título, autor, descripción, ingredientes y pasos, cada uno con su `label`.
  - CA-04: título, autor, ingredientes y pasos están marcados como obligatorios; descripción no.
  - CA-05: ingredientes y pasos son áreas de texto multilínea con una indicación de "uno por línea".
- **RF-03 — Validación**
  - CA-06: si falta un campo obligatorio, el formulario no se envía y se muestra un mensaje de error junto a ese campo.
  - CA-07: si se supera o no se alcanza la longitud permitida, se muestra un error que indica el límite.
  - CA-08: tras un error, todo lo escrito en los demás campos se conserva.
  - CA-09: la validación también ocurre en el servidor; un envío que se salte la validación del navegador recibe los mismos errores.
- **RF-04 — Publicación**
  - CA-10: al enviar un formulario válido se crea exactamente una receta en la base de datos.
  - CA-11: la fecha de publicación la asigna el servidor; el usuario no puede introducirla.
  - CA-12: tras publicar, se redirige a `/recetas/{id}/` de la nueva receta.

### 1.2 Listado de recetas
- **RF-05 — Listado**
  - CA-13: la página `/` muestra todas las recetas publicadas.
  - CA-14: las recetas aparecen ordenadas de la más reciente a la más antigua.
- **RF-06 — Elemento del listado**
  - CA-15: cada elemento muestra título, autor y fecha de publicación.
  - CA-16: el título enlaza a la página de detalle de esa receta.
- **RF-07 — Estado vacío**
  - CA-17: si no hay recetas, se muestra un mensaje que invita a publicar la primera, con enlace a `/recetas/nueva/`.

### 1.3 Detalle de receta
- **RF-08 — Detalle**
  - CA-18: se muestran título, autor, fecha, descripción (si existe), ingredientes y pasos.
  - CA-19: cada línea no vacía de ingredientes se muestra como un elemento de una lista con viñetas (`<ul>`).
  - CA-20: cada línea no vacía de pasos se muestra como un paso de una lista numerada (`<ol>`).
  - CA-21: si la receta no tiene descripción, no aparece ningún hueco ni texto vacío en su lugar.
- **RF-09 — URL propia**
  - CA-22: cada receta es accesible en `/recetas/{id}/` y la URL no cambia con el tiempo.
  - CA-23: al abrir esa URL directamente (sin pasar por el listado) se muestra la receta.
- **RF-10 — Volver al listado**
  - CA-24: el detalle incluye un enlace "← Volver" que lleva a `/`.
- **RF-11 — Página no encontrada**
  - CA-25: una receta o ruta inexistente devuelve el código HTTP 404 y la plantilla `404.html` propia, con enlace al inicio (con `DEBUG = False`).

### 1.4 Moderación
- **RF-13 — Admin de Django**
  - CA-26: el modelo `Receta` aparece en `/admin/` y se listan las recetas por título.
  - CA-27: el superusuario puede borrar una receta desde el admin y esta deja de aparecer en el listado y en su URL de detalle (que pasa a dar 404).
  - CA-28: un visitante sin iniciar sesión que entra en `/admin/` es redirigido a la pantalla de login del admin.

### 1.5 Foto de la receta (v1.1)
- **RF-12 — Foto**
  - CA-29: el formulario permite adjuntar una foto opcional en formato JPG, PNG o WebP de hasta 2 MB.
  - CA-30: la foto se muestra en el detalle y como miniatura en el listado, con el título de la receta como texto alternativo.
  - CA-31: una receta sin foto se muestra correctamente, sin imagen rota.

## 2. Formato Dado / Cuando / Entonces
Escenarios de los flujos principales del PRD.

- **ESC-01 — Publicar una receta válida** (CA-10, CA-11, CA-12)
  - **Dado** que estoy en `/recetas/nueva/`
  - **Cuando** relleno título "Tortilla de patatas", autor "Ana", ingredientes "Huevos⏎Patatas⏎Aceite⏎Sal" y pasos "Pelar las patatas⏎Freírlas⏎Batir los huevos⏎Cuajar la tortilla" y pulso "Publicar"
  - **Entonces** se crea la receta, soy redirigida a `/recetas/{id}/` y veo 4 ingredientes con viñetas y 4 pasos numerados.
- **ESC-02 — Publicar con un campo obligatorio vacío** (CA-06, CA-08)
  - **Dado** que estoy en `/recetas/nueva/`
  - **Cuando** relleno todo excepto los pasos y pulso "Publicar"
  - **Entonces** no se crea ninguna receta, veo un error junto al campo "Pasos" y el resto de campos conserva lo que escribí.
- **ESC-03 — Ver el listado ordenado** (CA-13, CA-14, CA-15)
  - **Dado** que existen las recetas "Pasta al pesto" (publicada ayer) y "Tortilla de patatas" (publicada hoy)
  - **Cuando** entro en `/`
  - **Entonces** veo "Tortilla de patatas" primero y "Pasta al pesto" después, cada una con su autor y su fecha.
- **ESC-04 — Listado vacío** (CA-17)
  - **Dado** que no hay ninguna receta publicada
  - **Cuando** entro en `/`
  - **Entonces** veo un mensaje que invita a publicar la primera receta y un enlace a `/recetas/nueva/`.
- **ESC-05 — Abrir el detalle desde el listado** (CA-16, CA-18, CA-24)
  - **Dado** que estoy en `/` y existe la receta "Tortilla de patatas"
  - **Cuando** pulso sobre su título
  - **Entonces** se abre su página de detalle con todo su contenido y un enlace "← Volver" que me devuelve a `/`.
- **ESC-06 — Abrir una receta que no existe** (CA-25)
  - **Dado** que no existe ninguna receta con id 9999
  - **Cuando** entro en `/recetas/9999/`
  - **Entonces** recibo un error 404 con la página propia y un enlace al inicio.
- **ESC-07 — Moderar una receta** (CA-27)
  - **Dado** que he iniciado sesión en `/admin/` como superusuario y existe una receta inapropiada
  - **Cuando** la borro desde el admin
  - **Entonces** ya no aparece en `/` y su URL de detalle devuelve 404.
- **ESC-08 — Acceso al admin sin permiso** (CA-28)
  - **Dado** que no he iniciado sesión
  - **Cuando** entro en `/admin/`
  - **Entonces** se me redirige a la pantalla de login y no veo ninguna receta.
- **ESC-09 — Publicar con foto (v1.1)** (CA-29, CA-30)
  - **Dado** que estoy en `/recetas/nueva/`
  - **Cuando** relleno los campos obligatorios, adjunto una foto JPG de 500 KB y pulso "Publicar"
  - **Entonces** la foto aparece en el detalle y como miniatura en el listado.

## 3. Casos límite y de error
- **Longitudes en el límite**
  - CL-01: un título de exactamente 3 y de exactamente 100 caracteres se acepta; uno de 2 o de 101 se rechaza con un mensaje de error.
  - CL-02: un autor de exactamente 2 y de exactamente 50 caracteres se acepta; uno de 1 o de 51 se rechaza.
  - CL-03: una descripción de 300 caracteres se acepta; una de 301 se rechaza.
  - CL-04: ingredientes de más de 3 000 caracteres o pasos de más de 5 000 se rechazan.
- **Contenido vacío o con espacios**
  - CL-05: un campo obligatorio que contiene solo espacios o saltos de línea se trata como vacío y se rechaza.
  - CL-06: las líneas vacías entre ingredientes o pasos se ignoran; no generan viñetas ni pasos numerados vacíos.
  - CL-07: los espacios al principio y al final de cada línea se eliminan al mostrarla.
- **Caracteres especiales y seguridad**
  - CL-08: tildes, eñes y emojis se guardan y se muestran correctamente.
  - CL-09: un texto como `<script>alert(1)</script>` en cualquier campo se muestra como texto literal y no se ejecuta (RNF-03).
  - CL-10: un envío del formulario sin token CSRF es rechazado con un error 403 y no crea ninguna receta (RNF-07).
  - CL-11: una palabra o URL muy larga sin espacios no rompe el diseño ni provoca desplazamiento horizontal.
- **URLs**
  - CL-12: `/recetas/abc/` (id no numérico) devuelve 404.
  - CL-13: `/recetas/0/` y `/recetas/-1/` devuelven 404.
  - CL-14: tras borrar una receta en el admin, su antigua URL devuelve 404.
- **Envíos**
  - CL-15: recargar la página de detalle justo después de publicar no crea una receta duplicada (patrón POST → redirección → GET).
  - CL-16: se permiten dos recetas con el mismo título; cada una tiene su propio id y su propia URL.
- **Foto (v1.1)**
  - CL-17: una foto de más de 2 MB se rechaza con un mensaje que indica el tamaño máximo.
  - CL-18: un archivo con formato no permitido (GIF, PDF) se rechaza.
  - CL-19: un archivo de texto renombrado como `.jpg` se rechaza porque Pillow no lo reconoce como imagen.
  - CL-20: si hay un error en otro campo, se indica al usuario que debe volver a adjuntar la foto (los navegadores no conservan los archivos tras recargar).

## 4. Criterios no funcionales medibles
- **Rendimiento**
  - CNF-01 (RNF-01): cada página carga en menos de 2 s en Chrome DevTools con el perfil de red "Fast 4G" y la caché desactivada.
  - CNF-02 (RNF-02): el peso total transferido de una página sin foto es inferior a 200 KB (pestaña Red de DevTools).
  - CNF-03: Lighthouse (móvil) da una puntuación de rendimiento de 90 o más en `/` y en el detalle.
- **Seguridad**
  - CNF-04 (RNF-03): no se usa el filtro `|safe` ni `mark_safe` con contenido de usuarios (revisión de código: 0 apariciones).
  - CNF-05 (RNF-05): no hay SQL escrito a mano (`raw()`, `cursor.execute`) en el código (0 apariciones).
  - CNF-06 (RNF-07): el formulario incluye `{% csrf_token %}` y `CsrfViewMiddleware` está activo en `settings.py`.
  - CNF-07 (RNF-08): en la configuración de despliegue, `python manage.py check --deploy` no muestra avisos críticos y `DEBUG = False`.
- **Accesibilidad**
  - CNF-08 (RNF-09 a RNF-13): Lighthouse da una puntuación de accesibilidad de 90 o más en todas las páginas.
  - CNF-09 (RNF-11): todas las acciones (publicar, abrir receta, volver) se pueden hacer solo con teclado y el foco es siempre visible.
  - CNF-10 (RNF-12): el contraste del texto es de al menos 4,5:1 y el texto principal mide 16 px o más.
- **SEO**
  - CNF-11 (RNF-14): cada página tiene un `<title>` y una `meta description` distintos; en el detalle contienen el título de la receta.
  - CNF-12 (RNF-16): con JavaScript desactivado, el listado y el detalle muestran todo su contenido.
  - CNF-13: Lighthouse da una puntuación de SEO de 90 o más.
- **Compatibilidad**
  - CNF-14 (RNF-17): los flujos 1, 2 y 3 del PRD funcionan en las 2 últimas versiones de Chrome, Firefox, Edge y Safari.
  - CNF-15 (RNF-18): a 360 px de ancho no hay desplazamiento horizontal y todos los elementos son legibles y pulsables.
- **Persistencia**
  - CNF-16 (RNF-19): tras detener y volver a arrancar el servidor (`runserver`), todas las recetas siguen apareciendo.

## 5. Definición de hecho (DoD)
Una funcionalidad se considera terminada cuando cumple todo lo siguiente:

- **Funcionalidad**
  - Cumple todos sus criterios de aceptación (sección 1) y sus escenarios (sección 2).
  - Sus casos límite y de error (sección 3) están comprobados.
- **Código**
  - El código está en `src/` y sigue la estructura definida en [scope.md](scope.md).
  - Los cambios en el modelo tienen su migración creada (`makemigrations`) y aplicada (`migrate`).
  - `python manage.py check` se ejecuta sin errores.
  - No quedan `print()` de depuración ni código comentado sin uso.
- **Pruebas**
  - Tiene pruebas automáticas en `recetas/tests.py` y `python manage.py test` pasa al 100 %.
  - Se ha probado a mano en escritorio y en móvil (o con la vista móvil de DevTools a 360 px).
- **Calidad**
  - Respeta los criterios no funcionales que le afectan (sección 4).
  - Respeta el estilo minimalista y los principios de [vision.md](vision.md).
- **Documentación y entrega**
  - Si cambió algo del comportamiento, se han actualizado el PRD, el alcance y este documento.
  - `README.md` explica cómo instalar y ejecutar el proyecto con el estado actual.
  - Los cambios están guardados en Git con un mensaje descriptivo.

## 6. Pruebas de aceptación

### 6.1 Pruebas manuales
Se ejecutan antes de cada entrega con el servidor en marcha (`python manage.py runserver`).

- **PA-01 — Publicar una receta** (ESC-01)
  1. Abrir `/` y pulsar "Nueva receta".
  2. Rellenar los campos obligatorios con datos válidos y pulsar "Publicar".
  3. **Resultado esperado:** se abre el detalle de la receta con ingredientes en viñetas y pasos numerados.
- **PA-02 — Errores de validación** (ESC-02, CL-01, CL-05)
  1. En `/recetas/nueva/`, dejar los pasos vacíos y escribir un título de 2 caracteres.
  2. Pulsar "Publicar".
  3. **Resultado esperado:** dos mensajes de error junto a sus campos, el resto de datos conservado y ninguna receta nueva en `/`.
- **PA-03 — Listado y orden** (ESC-03, ESC-04)
  1. Con la base de datos vacía, abrir `/` y comprobar el mensaje de estado vacío.
  2. Publicar dos recetas seguidas.
  3. **Resultado esperado:** la última publicada aparece la primera, con título, autor y fecha.
- **PA-04 — Detalle y navegación** (ESC-05, CA-23)
  1. Pulsar una receta del listado, copiar su URL, pulsar "← Volver" y pegar la URL en una pestaña nueva.
  2. **Resultado esperado:** el detalle se ve igual en ambos casos y "← Volver" lleva a `/`.
- **PA-05 — Página 404** (ESC-06, CL-12)
  1. Con `DEBUG = False`, abrir `/recetas/9999/` y `/recetas/abc/`.
  2. **Resultado esperado:** la página 404 propia con enlace al inicio en ambos casos.
- **PA-06 — Seguridad XSS** (CL-09)
  1. Publicar una receta con `<script>alert(1)</script>` como título.
  2. **Resultado esperado:** el texto se ve literal en el listado y en el detalle, y no aparece ninguna alerta.
- **PA-07 — Moderación** (ESC-07, ESC-08)
  1. En una ventana privada, abrir `/admin/` y comprobar la redirección al login.
  2. Iniciar sesión como superusuario, borrar una receta y volver a `/`.
  3. **Resultado esperado:** la receta ya no aparece y su URL devuelve 404.
- **PA-08 — Responsive y teclado** (CNF-09, CNF-15)
  1. Con la vista móvil a 360 px, recorrer listado, formulario y detalle.
  2. Repetir el flujo de publicar usando solo el teclado (Tab, Enter).
  3. **Resultado esperado:** sin desplazamiento horizontal, todo legible y el flujo se completa sin ratón.
- **PA-09 — Rendimiento, accesibilidad y SEO** (CNF-01 a CNF-03, CNF-08, CNF-13)
  1. Ejecutar Lighthouse en modo móvil sobre `/` y sobre un detalle.
  2. **Resultado esperado:** 90 o más en Rendimiento, Accesibilidad y SEO, y carga en menos de 2 s.
- **PA-10 — Persistencia** (CNF-16)
  1. Publicar una receta, detener el servidor y volver a arrancarlo.
  2. **Resultado esperado:** la receta sigue en el listado.
- **PA-11 — Foto (v1.1)** (ESC-09, CL-17, CL-18)
  1. Publicar una receta con una foto JPG válida; intentar otra con una foto de 3 MB y otra con un GIF.
  2. **Resultado esperado:** la primera se publica con su foto; las otras dos se rechazan con un mensaje claro.

### 6.2 Pruebas automáticas
Se escriben en `src/recetas/tests.py` con `django.test.TestCase` y el cliente de pruebas de Django, y se ejecutan con `python manage.py test`.

- **Modelo**
  - `test_orden_por_fecha_descendente`: las recetas se devuelven de la más reciente a la más antigua (CA-14).
  - `test_get_absolute_url`: devuelve `/recetas/{id}/` (CA-22).
  - `test_lista_ingredientes_ignora_lineas_vacias`: las líneas vacías y los espacios sobrantes se descartan (CL-06, CL-07).
- **Formulario**
  - `test_formulario_valido`: con datos correctos, el formulario es válido (CA-10).
  - `test_campos_obligatorios`: sin título, autor, ingredientes o pasos, el formulario es inválido (CA-06).
  - `test_solo_espacios_es_invalido`: un campo con solo espacios se rechaza (CL-05).
  - `test_longitudes_limite`: se aceptan los valores en el límite y se rechazan los que lo superan (CL-01 a CL-04).
- **Vistas**
  - `test_listado_vacio_muestra_mensaje`: `/` responde 200 y muestra el mensaje de estado vacío (CA-17).
  - `test_listado_muestra_recetas`: `/` muestra título, autor y fecha de cada receta (CA-13, CA-15).
  - `test_crear_receta_redirige_al_detalle`: un POST válido crea 1 receta y redirige a su detalle (CA-10, CA-12).
  - `test_crear_receta_invalida_no_guarda`: un POST inválido responde 200, muestra errores y no crea recetas (CA-06, CA-08).
  - `test_detalle_muestra_listas`: el detalle contiene un `<ul>` con los ingredientes y un `<ol>` con los pasos (CA-19, CA-20).
  - `test_detalle_inexistente_404`: `/recetas/9999/` responde 404 (CA-25, CL-13).
  - `test_contenido_escapado`: un título con `<script>` aparece escapado en la respuesta (CL-09).
  - `test_post_sin_csrf_rechazado`: con `Client(enforce_csrf_checks=True)`, un POST sin token responde 403 (CL-10).
- **Admin**
  - `test_admin_requiere_login`: `/admin/` redirige al login si no hay sesión (CA-28).
  - `test_receta_registrada_en_admin`: `Receta` está registrada en el sitio de administración (CA-26).
