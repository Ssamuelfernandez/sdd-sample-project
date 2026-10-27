# PRD — Blog de Cocina

## 1. Resumen ejecutivo
El Blog de Cocina es una aplicación web minimalista que permite a cualquier visitante **publicar recetas** mediante un único formulario y **leer** las recetas publicadas por otras personas. La v1 incluye solo tres cosas: un formulario de publicación, un listado de recetas en la página principal y una página de detalle por receta. No hay registro, me gusta, comentarios ni publicidad. El objetivo es que publicar lleve menos de 2 minutos y que leer una receta sea cómodo en cualquier dispositivo, siguiendo los principios de [vision.md](spec/vision.md).

## 2. Usuarios y personas
- **Ana — Autora (34 años, cocinera casera)**
  - **Perfil:** cocina a diario en casa y tiene varias recetas familiares que le piden a menudo. Usa el móvil y el ordenador a nivel básico.
  - **Objetivos:**
    - Compartir sus recetas con amigos y desconocidos de forma rápida.
    - Tener sus recetas publicadas en un sitio ordenado y fácil de enlazar.
  - **Frustraciones:**
    - Las webs de recetas le piden crear una cuenta y rellenar muchos campos.
    - En redes sociales sus recetas se pierden y la gente le vuelve a preguntar por los ingredientes.
- **Luis — Lector (27 años, cocina para él y su pareja)**
  - **Perfil:** cocina varias veces por semana y busca ideas nuevas. Consulta las recetas en el móvil, apoyado en la encimera.
  - **Objetivos:**
    - Encontrar rápidamente qué cocinar hoy.
    - Seguir los pasos de una receta sin perderse mientras cocina.
  - **Frustraciones:**
    - Tener que pasar por anuncios e historias largas antes de llegar a la receta.
    - Páginas lentas o que se mueven al cargar publicidad.

> En la v1 no hay diferencia técnica entre autor y lector: cualquier visitante puede publicar y leer.

## 3. Casos de uso / historias de usuario
- **HU-01:** Como **autora**, quiero rellenar un formulario con el título, mis datos, los ingredientes y los pasos, para publicar mi receta.
- **HU-02:** Como **autora**, quiero que se me avise de forma clara si falta algún dato obligatorio, para corregirlo sin perder lo que ya he escrito.
- **HU-03:** Como **autora**, quiero ver mi receta publicada justo después de enviarla, para comprobar que se ve bien.
- **HU-04:** Como **lector**, quiero ver en la página principal todas las recetas, de la más reciente a la más antigua, para elegir qué cocinar.
- **HU-05:** Como **lector**, quiero abrir una receta y ver sus ingredientes en lista y sus pasos numerados, para seguirla mientras cocino.
- **HU-06:** Como **lector**, quiero que cada receta tenga su propio enlace, para guardarla o enviársela a alguien.
- **HU-07:** Como **autora**, quiero añadir una foto a mi receta, para que resulte más apetecible.
- **HU-08:** Como **responsable del blog**, quiero una API con la que otros programas lean las recetas publicadas y creen borradores con mi token, para integrar el blog con scripts y herramientas sin pasar por el navegador.

## 4. Requisitos funcionales
Prioridades: **imprescindible** (sin esto no hay v1) · **deseable** (debería estar en la v1) · **opcional** (puede posponerse).

- **RF-01 — Acceso al formulario** · Prioridad: imprescindible · HU-01
  - Un botón "Nueva receta" visible en la cabecera de todas las páginas lleva al formulario de publicación.
- **RF-02 — Campos de la receta** · Prioridad: imprescindible · HU-01
  - Campos obligatorios: título, autor, ingredientes y pasos.
  - Campo opcional: descripción corta.
  - Ingredientes y pasos se escriben uno por línea.
- **RF-03 — Validación** · Prioridad: imprescindible · HU-02
  - Se valida en el servidor con un formulario de Django (`ModelForm`) según las reglas del modelo de datos.
  - En el navegador se valida con los atributos HTML (`required`, `maxlength`) que Django genera a partir del formulario.
  - Si hay errores, se muestra un mensaje junto a cada campo afectado y se conserva todo lo escrito.
- **RF-04 — Publicación** · Prioridad: imprescindible · HU-03
  - Al enviar un formulario válido, la receta se guarda con la fecha y hora de publicación asignadas por el servidor.
  - A continuación se redirige a la página de detalle de la nueva receta.
- **RF-05 — Listado de recetas** · Prioridad: imprescindible · HU-04
  - La página principal muestra todas las recetas ordenadas por fecha de publicación, de la más reciente a la más antigua.
- **RF-06 — Elemento del listado** · Prioridad: imprescindible · HU-04
  - Cada receta del listado muestra título, autor y fecha, y enlaza a su página de detalle.
- **RF-07 — Estado vacío** · Prioridad: deseable · HU-04
  - Si no hay recetas, se muestra un mensaje que invita a publicar la primera, con enlace al formulario.
- **RF-08 — Detalle de receta** · Prioridad: imprescindible · HU-05
  - Muestra título, autor, fecha, descripción (si existe), ingredientes como lista con viñetas y pasos como lista numerada.
- **RF-09 — URL propia** · Prioridad: imprescindible · HU-06
  - Cada receta tiene una URL única y estable con el formato `/recetas/{id}/`.
- **RF-10 — Volver al listado** · Prioridad: deseable · HU-05
  - La página de detalle incluye un enlace "← Volver" a la página principal.
- **RF-11 — Página no encontrada** · Prioridad: deseable · HU-06
  - Una receta o ruta inexistente muestra una página 404 propia (plantilla `404.html`) con enlace al inicio.
- **RF-12 — Foto de la receta** · Prioridad: opcional · HU-07
  - El formulario permite subir una foto (JPG, PNG o WebP, máximo 2 MB) mediante un `ImageField`.
  - La foto se muestra en el detalle y como miniatura en el listado.
- **RF-13 — Moderación** · Prioridad: deseable · Riesgo de spam
  - El modelo `Receta` se registra en el panel de administración de Django (`/admin/`).
  - Solo el responsable del blog (superusuario) puede entrar para revisar y borrar recetas; no es visible para los visitantes.
- **RF-14 — API REST** · Prioridad: opcional · HU-08
  - Se ofrece con Django REST Framework bajo `/api/recetas/`:
    - `GET /api/recetas/`: lista las recetas publicadas (`publicada=True`), de la más reciente a la más antigua.
    - `GET /api/recetas/{id}/`: devuelve una receta publicada; un borrador o un id inexistente dan 404.
    - `POST /api/recetas/`: crea una receta **siempre como borrador** (`publicada=False`).
  - Contrato JSON: el POST recibe `titulo`, `autor`, `ingredientes`, `pasos` y, opcional, `descripcion`. Las respuestas incluyen `id`, `titulo`, `autor`, `descripcion`, `ingredientes`, `pasos` y `estado` (`publicada` o `borrador`).
  - Se aplican las mismas validaciones que en el formulario web (RF-03); los errores devuelven 400 con un mensaje por campo. La API no admite `imagen`.
  - Los GET son públicos. El POST exige un token (`Authorization: Token <token>`) de un usuario administrador de Django (`is_staff`): sin token 401, sin permisos 403. No se crean nuevos sistemas de usuarios.
  - No modifica el modelo `Receta`: cualquier valor de `estado` o `publicada` enviado por el cliente se ignora.

## 5. Requisitos no funcionales
- **Rendimiento**
  - RNF-01: cualquier página carga en menos de 2 s con una conexión 4G estándar.
  - RNF-02: las páginas no dependen de librerías JavaScript pesadas; el peso total de una página sin foto es inferior a 200 KB.
- **Seguridad**
  - RNF-03: todo el texto introducido por los usuarios se escapa antes de mostrarse, para evitar XSS. Se usa el autoescapado de las plantillas de Django y no se usa el filtro `|safe` con contenido de usuarios.
  - RNF-04: los datos se validan siempre en el servidor con el formulario de Django, aunque ya se hayan validado en el navegador.
  - RNF-05: el acceso a la base de datos se hace solo con el ORM de Django, sin SQL escrito a mano (prevención de inyección SQL).
  - RNF-06: las fotos subidas se aceptan solo con formato y tamaño permitidos, se validan con Pillow y se guardan en `MEDIA_ROOT` con un nombre generado por el servidor.
  - RNF-07: el formulario de publicación incluye el token CSRF de Django (`{% csrf_token %}`).
  - RNF-08: en un despliegue público, `DEBUG = False`, `SECRET_KEY` fuera del código (variable de entorno) y `ALLOWED_HOSTS` configurado.
- **Accesibilidad**
  - RNF-09: HTML semántico (`header`, `main`, `article`, `ol`, `ul`).
  - RNF-10: todos los campos del formulario tienen `label` y los errores se asocian a su campo.
  - RNF-11: la web se puede usar entera con teclado y con el foco visible.
  - RNF-12: el contraste de texto cumple el nivel WCAG AA y el texto principal mide al menos 16 px.
  - RNF-13: las fotos llevan texto alternativo (por defecto, el título de la receta).
- **SEO**
  - RNF-14: cada página tiene un `<title>` y una `meta description` propios (en el detalle, el título y la descripción de la receta), definidos mediante bloques de la plantilla base.
  - RNF-15: URLs limpias y estables (RF-09).
  - RNF-16: el contenido se renderiza en el servidor con plantillas de Django, de modo que los buscadores lo leen sin ejecutar JavaScript.
- **Compatibilidad**
  - RNF-17: funciona en las 2 últimas versiones de Chrome, Firefox, Edge y Safari.
  - RNF-18: diseño responsive usable desde 360 px de ancho hasta escritorio.
- **Persistencia**
  - RNF-19: las recetas se conservan tras reiniciar el servidor (base de datos SQLite gestionada con migraciones de Django).

## 6. Flujos principales
- **Flujo 1 — Publicar una receta**
  1. La usuaria pulsa **"Nueva receta"** en la cabecera.
  2. Se abre el formulario (`/recetas/nueva/`).
  3. Rellena título, autor, ingredientes (uno por línea), pasos (uno por línea) y, si quiere, la descripción.
  4. Pulsa **"Publicar"**.
  5. Si hay errores → el formulario se vuelve a mostrar con los mensajes junto a cada campo y con lo escrito intacto; vuelve al paso 3.
  6. Si todo es válido → se guarda la receta y se redirige a `/recetas/{id}/`.
- **Flujo 2 — Explorar y leer una receta**
  1. El usuario entra en la página principal (`/`).
  2. Ve el listado de recetas, de la más reciente a la más antigua.
  3. Pulsa sobre el título de una receta.
  4. Se abre `/recetas/{id}/` con ingredientes en lista y pasos numerados.
  5. Pulsa **"← Volver"** para regresar al listado.
- **Flujo 3 — Acceder a un enlace inexistente**
  1. El usuario abre una URL de receta que no existe.
  2. Se muestra la página 404 con un enlace a la página principal.

## 7. Modelo de datos inicial
- **Modelo de Django `Receta`** (app `recetas`, única entidad de la v1)
  - **`id`** — `BigAutoField`, generado automáticamente por Django.
  - **`titulo`** — `CharField(max_length=100)`, obligatorio, mínimo 3 caracteres (`MinLengthValidator`).
  - **`autor`** — `CharField(max_length=50)`, obligatorio, mínimo 2 caracteres.
  - **`descripcion`** — `CharField(max_length=300, blank=True)`, opcional.
  - **`ingredientes`** — `TextField`, obligatorio, al menos 1 línea no vacía, máximo 3 000 caracteres.
  - **`pasos`** — `TextField`, obligatorio, al menos 1 línea no vacía, máximo 5 000 caracteres.
  - **`imagen`** — `ImageField(upload_to="recetas/", blank=True)`, opcional; solo se usa si se implementa RF-12 (requiere Pillow).
  - **`fecha_publicacion`** — `DateTimeField(auto_now_add=True)`, asignada automáticamente al crear.
  - **Comportamiento del modelo**
    - `Meta.ordering = ["-fecha_publicacion"]`, que da el orden del listado (RF-05).
    - `__str__` devuelve el título, que es como se ve la receta en el admin.
    - `get_absolute_url()` devuelve `/recetas/{id}/`, a donde se redirige tras publicar (RF-04).
    - Métodos auxiliares `lista_ingredientes()` y `lista_pasos()`, que separan el texto por líneas para mostrarlo como listas (RF-08).
- **Relaciones**
  - En la v1 no hay relaciones: el autor es un texto libre dentro de la receta.
  - **Previsto para v2:** relación **1 a N** entre el `User` de Django (`django.contrib.auth`) y `Receta`, mediante un `ForeignKey` (un usuario publica muchas recetas; cada receta pertenece a un usuario).

## 8. Dependencias y supuestos
- **Dependencias**
  - Python y Django, según el stack definido en [scope.md](spec/scope.md).
  - SQLite, que viene incluido con Python y es la base de datos por defecto de Django.
  - Pillow, solo si se implementa RF-12 (lo necesita `ImageField`).
  - Django REST Framework (`djangorestframework`), solo para RF-14, con su app `rest_framework.authtoken` para los tokens.
  - Apps incluidas en Django: `django.contrib.admin` (moderación, RF-13), `auth` y `sessions` (las necesita el admin) y `staticfiles` (CSS).
  - No se usa ningún servicio externo de pago ni API de terceros.
- **Supuestos**
  - No hay login para los visitantes: el autor se identifica solo con el nombre que escribe. Solo el responsable del blog tiene un superusuario para el admin.
  - El volumen de recetas y visitas es bajo (proyecto de clase), por lo que no hacen falta paginación ni caché.
  - Los usuarios publican contenido de buena fe; la moderación, si hace falta, se hace desde el panel de administración de Django.
  - Hay un entorno (local o servidor sencillo) con almacenamiento persistente para la base de datos y las fotos.

## 9. Riesgos
- **Spam o contenido inapropiado (no hay login)**
  - Probabilidad: media · Impacto: medio.
  - Mitigación: límites de longitud en los campos; borrado desde el admin de Django (RF-13); valorar un control antispam sencillo en v2.
- **Ataques XSS, inyección SQL o CSRF a través del formulario**
  - Probabilidad: media · Impacto: alto.
  - Mitigación: RNF-03 a RNF-07 (autoescapado de plantillas, validación con formularios de Django, uso exclusivo del ORM y token CSRF).
- **Configuración insegura al desplegar (`DEBUG` activo, clave secreta expuesta)**
  - Probabilidad: media · Impacto: alto.
  - Mitigación: RNF-08 y revisión con `python manage.py check --deploy` antes de publicar.
- **Crecimiento del alcance durante el desarrollo**
  - Probabilidad: alta · Impacto: medio.
  - Mitigación: seguir las reglas de cambio de [scope.md](spec/scope.md) y el principio "Simple antes que completo".
- **No llegar a tiempo con la v1**
  - Probabilidad: media · Impacto: alto.
  - Mitigación: construir primero los requisitos imprescindibles; los deseables y opcionales se pueden recortar.
- **Uso indebido de la API o fuga del token de administrador**
  - Probabilidad: baja · Impacto: medio.
  - Mitigación: los GET no exponen borradores; el POST solo crea borradores y exige token de administrador; el token se puede regenerar desde el admin (RF-14).
- **Fotos pesadas que ralentizan la web**
  - Probabilidad: baja · Impacto: bajo.
  - Mitigación: límite de 2 MB y formatos permitidos (RF-12, RNF-06).
- **Las fotos subidas no se ven en desarrollo**
  - Probabilidad: media · Impacto: bajo.
  - Mitigación: configurar `MEDIA_URL` y `MEDIA_ROOT` y servir los archivos de media con `static()` en `urls.py` cuando `DEBUG = True`.

## 10. Métricas de éxito
Cada métrica mide un objetivo del [briefing](briefing.md).

- **OBJ-1 — Publicar en menos de 2 minutos**
  - Métrica: tiempo que tarda una persona nueva, sin ayuda, desde que pulsa "Nueva receta" hasta ver su receta publicada.
  - Objetivo: menos de 2 minutos en al menos el 80 % de las pruebas con usuarios.
- **OBJ-2 — Ver todas las recetas y su detalle**
  - Métrica: porcentaje de recetas publicadas que aparecen en el listado y abren correctamente su detalle.
  - Objetivo: 100 %, verificado con los criterios de aceptación.
- **OBJ-3 — Lectura cómoda y sin distracciones**
  - Métrica: tiempo de carga de las páginas y valoración de facilidad de uso en pruebas con usuarios (escala 1–5).
  - Objetivo: carga en menos de 2 s y valoración media de 4 o más.
- **OBJ-4 — MVP terminado a tiempo**
  - Métrica: requisitos imprescindibles (RF-01, RF-02, RF-03, RF-04, RF-05, RF-06, RF-08, RF-09) completados y aceptados en la fecha de entrega.
  - Objetivo: 100 % de los imprescindibles.
