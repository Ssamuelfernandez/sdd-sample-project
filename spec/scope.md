# Alcance — Blog de Cocina

## 1. Dentro del alcance (v1)
- **Publicar recetas**
  - RF-01 — Acceso al formulario desde la cabecera.
  - RF-02 — Campos de la receta (título, autor, ingredientes, pasos y descripción opcional).
  - RF-03 — Validación con `ModelForm` de Django, conservando lo escrito.
  - RF-04 — Publicación con fecha automática y redirección al detalle.
- **Ver el listado**
  - RF-05 — Listado en la página principal, de la más reciente a la más antigua.
  - RF-06 — Cada elemento muestra título, autor y fecha.
  - RF-07 — Mensaje de estado vacío.
- **Ver el detalle**
  - RF-08 — Detalle con ingredientes en lista y pasos numerados.
  - RF-09 — URL propia `/recetas/{id}/`.
  - RF-10 — Enlace "← Volver" al listado.
  - RF-11 — Página 404 propia.
- **Moderación**
  - RF-13 — Modelo `Receta` registrado en el admin de Django, accesible solo para el superusuario.
- **API REST (opcional, hito 9)**
  - RF-14 — `GET /api/recetas/`, `GET /api/recetas/{id}/` y `POST /api/recetas/` (solo crea borradores, con token de administrador).
- **Requisitos no funcionales**
  - RNF-01 a RNF-19 del [PRD](../PRD.md): rendimiento, seguridad, accesibilidad, SEO, compatibilidad y persistencia.
- **Pantallas incluidas**
  - `/` — Listado de recetas.
  - `/recetas/nueva/` — Formulario de nueva receta.
  - `/recetas/{id}/` — Detalle de receta.
  - 404 — Página no encontrada.
  - `/admin/` — Panel de administración de Django (solo para el responsable del blog).
  - `/api/recetas/` y `/api/recetas/{id}/` — API REST (RF-14).

## 2. Fuera del alcance
Exclusiones permanentes: no está previsto hacerlas.

- **Publicidad**
  - Motivo: contradice la propuesta de valor ("leer sin ruido") y el principio "La receta es la protagonista".
- **Panel de administración propio o para los visitantes**
  - Motivo: el admin que trae Django ya cubre la moderación (RF-13); construir otro panel añadiría complejidad sin valor para el usuario.
- **Aplicación móvil nativa**
  - Motivo: la web responsive cubre el uso en móvil; una app duplicaría el trabajo.
- **Frontend SPA (React, Vue, etc.)**
  - Motivo: va contra el principio "Ligero y rápido"; el renderizado en el servidor cubre todas las necesidades y favorece el SEO.
- **Multidioma**
  - Motivo: el público objetivo es hispanohablante; traducir la interfaz no aporta valor ahora.
- **Analítica y seguimiento de usuarios**
  - Motivo: va contra el principio "Ligero y rápido" y no es necesaria para medir el éxito (se mide con pruebas con usuarios).
- **Newsletter y notificaciones**
  - Motivo: requieren datos de contacto y cuentas, ajenos a la idea de publicar y leer.

## 3. Aplazado a versiones futuras
Funcionalidades que sí se quieren, pero no en la v1 (ver la hoja de ruta en [vision.md](vision.md)).

- **v1.1**
  - RF-12 — Foto de la receta (prioridad opcional en el PRD; requiere Pillow y configurar `MEDIA_ROOT`).
- **v2**
  - Editar y borrar recetas propias.
  - Identificación mínima del autor (cuentas con `django.contrib.auth` o enlace privado de edición), necesaria para lo anterior.
- **Futuro (sin compromiso)**
  - Categorías y buscador.
  - Paginación del listado (con el `Paginator` de Django), si el número de recetas crece.
  - Campos extra: tiempo de preparación y raciones.
  - Favoritos, versión imprimible y modo oscuro.
  - Me gusta y comentarios.

## 4. Supuestos
- Cualquier visitante puede publicar sin registrarse; el autor es un nombre libre.
- El único usuario registrado es el superusuario del responsable del blog, que se crea con `createsuperuser`.
- Habrá pocas recetas y pocas visitas, así que no hacen falta paginación, caché ni escalado.
- Los usuarios publican de buena fe; el contenido inapropiado se borra desde el admin de Django.
- Se dispone de un entorno (local o servidor sencillo) con Python instalado y disco persistente.
- El plazo de la clase permite completar al menos todos los requisitos imprescindibles.

## 5. Restricciones técnicas
- **Stack cerrado**
  - Lenguaje: Python 3.12 o superior.
  - Framework: Django 5.2 (LTS).
  - Vistas: vistas genéricas basadas en clases (`ListView`, `CreateView`, `DetailView`).
  - Plantillas: sistema de plantillas de Django, renderizado en el servidor (sin SPA ni paso de compilación).
  - Formularios: `ModelForm` de Django.
  - Base de datos: SQLite (`db.sqlite3`), gestionada con el ORM y las migraciones de Django.
  - Estilos: CSS propio, sin frameworks, servido con `django.contrib.staticfiles`.
  - Fotos (solo v1.1): `ImageField` + Pillow, guardadas en `MEDIA_ROOT/recetas/`.
  - API (RF-14): Django REST Framework con autenticación por token (`rest_framework.authtoken`); la web sigue renderizándose en el servidor con plantillas.
  - Dependencias declaradas en `requirements.txt`; desarrollo dentro de un entorno virtual (`venv`).
- **Límites de la plataforma**
  - Sin servicios de pago ni APIs externas.
  - SQLite admite una sola escritura a la vez; es suficiente para el volumen previsto.
  - La página 404 propia solo se ve con `DEBUG = False`; con `DEBUG = True` Django muestra su página de depuración.
  - En desarrollo, Django sirve los archivos estáticos y de media; en un despliegue público hay que configurar `collectstatic` y el servidor web.
  - Las fotos se guardan en el disco del servidor, con un máximo de 2 MB por foto.
- **Estructura prevista de `src/`**
  ```
  src/
    manage.py
    requirements.txt
    db.sqlite3              → se crea al ejecutar las migraciones (no se sube a Git)
    blog_cocina/            → proyecto Django
      settings.py
      urls.py               → incluye las URLs de la app y del admin
      wsgi.py
    recetas/                → app de recetas
      models.py             → modelo Receta
      forms.py              → RecetaForm (ModelForm)
      views.py              → ListView, CreateView, DetailView
      urls.py               → "", "recetas/nueva/", "recetas/<int:pk>/"
      admin.py              → registro de Receta en el admin
      migrations/
      templates/recetas/
        receta_list.html    → listado
        receta_form.html    → formulario
        receta_detail.html  → detalle
    templates/
      base.html             → layout común con cabecera
      404.html
    static/
      css/styles.css
    media/
      recetas/              → fotos subidas (v1.1, no se sube a Git)
  ```

## 6. Hitos y entregables
1. **Hito 1 — Documentación**
   - Entregables: `briefing.md`, `PRD.md`, `spec/vision.md`, `spec/scope.md` y `spec/acceptance_criteria.md` revisados.
2. **Hito 2 — Base del proyecto**
   - Entregables: entorno virtual y `requirements.txt`; proyecto `blog_cocina` (`startproject`) y app `recetas` (`startapp`); modelo `Receta` con su migración aplicada; plantilla `base.html` con cabecera.
3. **Hito 3 — Publicar recetas**
   - Entregables: RF-01, RF-02, RF-03 y RF-04 funcionando (`RecetaForm` + `CreateView`).
4. **Hito 4 — Ver recetas**
   - Entregables: RF-05, RF-06, RF-07, RF-08, RF-09, RF-10 y RF-11 funcionando (`ListView`, `DetailView` y `404.html`).
5. **Hito 5 — Moderación**
   - Entregables: RF-13 (`admin.py` configurado y superusuario creado).
6. **Hito 6 — Estilo y calidad**
   - Entregables: CSS minimalista y responsive; revisión de los RNF (seguridad, accesibilidad, SEO, rendimiento); `python manage.py check` sin errores.
7. **Hito 7 — Entrega de la v1**
   - Entregables: criterios de aceptación verificados; `README.md` con instrucciones (crear el `venv`, `pip install -r requirements.txt`, `migrate`, `createsuperuser`, `runserver`); código final en `src/`.
8. **Hito 8 — v1.1 (si hay tiempo)**
   - Entregables: RF-12 (foto de la receta con `ImageField`, Pillow y configuración de media).
9. **Hito 9 — API REST (opcional)**
   - Entregables: RF-14 (serializador, vistas y rutas de `/api/recetas/`, token de administrador, pruebas de API y ejemplos `curl` en el `README.md`). Cambio aprobado según la sección 7: no desplaza ningún requisito imprescindible y reutiliza el modelo `Receta` sin migraciones propias.

## 7. Reglas de cambio
1. **Proponer:** cualquier idea nueva se anota primero en "Dudas abiertas" del [briefing](../briefing.md); no se programa directamente.
2. **Evaluar con la visión:** se contrasta con los principios de [vision.md](vision.md). Si contradice "Simple antes que completo" o "La receta es la protagonista", se rechaza.
3. **Evaluar el coste:** si entra en la v1, hay que indicar qué requisito deseable u opcional se retrasa para compensar el tiempo; los imprescindibles no se tocan. Se da preferencia a las soluciones que ya trae Django antes que a paquetes externos.
4. **Decidir dónde va:**
   - Aprobada para v1 → se añade como nuevo RF en el PRD y en la sección 1 de este documento.
   - Aprobada para más adelante → se añade a "Aplazado a versiones futuras".
   - Rechazada → se añade a "Fuera del alcance" con su motivo.
5. **Actualizar los documentos:** antes de programar, se actualizan el PRD, este alcance y los criterios de aceptación. Si el cambio afecta al modelo `Receta`, se crea su migración.
