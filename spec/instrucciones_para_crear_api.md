# Incorporar API REST al Blog de Cocina

Actúa como desarrollador experto en Django y SDD (Spec-Driven Development).

Analiza el repositorio, especialmente `src/recetas/`, `PRD.md` y `spec/`. **Actualiza primero las especificaciones y después implementa la API.**

## 0. Proceso SDD (obligatorio)

Sigue las "Reglas de cambio" de `spec/scope.md` (sección 7):

- Anota la idea en "Dudas abiertas" de `briefing.md` y contrástala con `spec/vision.md` (principio "Simple antes que completo").
- Añade una nueva historia de usuario (**HU-08**) y un nuevo requisito funcional (**RF-14**, prioridad opcional) en `PRD.md`, con su hito en `spec/scope.md`. Indica qué se aplaza si hace falta compensar tiempo.
- Añade en `spec/acceptance_criteria.md` los criterios (**CA-32** en adelante), escenarios (**ESC-10** en adelante), casos límite (**CL-21** en adelante) y pruebas (**PA-12** en adelante), continuando la numeración actual y manteniendo la trazabilidad.
- Solo después, implementa en `src/`.

## 1. API

Utiliza Django REST Framework e incorpora, bajo `/api/`:

- `GET /api/recetas/`: listar las recetas publicadas (`publicada=True`), de la más reciente a la más antigua.
- `GET /api/recetas/{id}/`: consultar una receta publicada.
- `POST /api/recetas/`: crear una receta como borrador.

## 2. Contrato JSON

- El POST recibe `titulo`, `autor`, `ingredientes` y `pasos` (obligatorios) y, opcionalmente, `descripcion`.
- La respuesta (en GET y POST) incluye `id`, `titulo`, `autor`, `descripcion`, `ingredientes`, `pasos` y `estado` (`publicada` o `borrador`).
- Aplica las mismas validaciones que el formulario web (RF-03): longitudes mínimas y máximas de cada campo. Los errores se devuelven con `400` y un mensaje por campo, en español.
- No se admite subir `imagen` por la API en esta versión.

## 3. Modelo

Conserva `Receta` y su campo `publicada`. El POST siempre guardará `publicada=False`, ignorando cualquier valor de `estado` o `publicada` que envíe el cliente. `fecha_publicacion` se completa sola (`auto_now_add`) y `imagen` queda vacía (se mostrará la imagen genérica). Evita modificar el modelo o crear migraciones salvo que sean imprescindibles.

## 4. Seguridad

- Los GET son públicos y excluyen borradores: pedir un borrador por id devuelve `404`, igual que en la web.
- El POST requiere un token de un usuario administrador de Django (`is_staff`), enviado como `Authorization: Token <token>`, usando `rest_framework.authtoken`. Sin token → `401`; con token de un usuario no administrador → `403`.
- No implementes nuevos sistemas de usuarios: el token se genera para el superusuario existente (admin de Django o `manage.py drf_create_token <usuario>`).

## 5. Compatibilidad

Conserva la web (portada, detalle, formulario, borradores), el Django Admin y las 9 recetas existentes. Añade `djangorestframework` a `src/requirements.txt` y registra `rest_framework` y `rest_framework.authtoken` en `INSTALLED_APPS` (la app `authtoken` sí necesita su migración, que es de la librería y no del modelo `Receta`). Mantén el código en el estilo actual del proyecto (español, comentarios breves) y prefiere las soluciones que ya trae DRF (`ModelSerializer`, vistas genéricas).

## 6. Verificación

- Ejecuta las pruebas existentes (`python manage.py test`) y confirma que siguen pasando.
- Añade pruebas de:
  - **API:** listado, detalle y creación correctos, y orden del listado.
  - **Permisos:** POST sin token (401), con token de no administrador (403) y con token de administrador (201).
  - **Validación:** campos obligatorios ausentes, título o autor demasiado cortos, textos por encima del máximo.
  - **Regresión:** un POST con `publicada: true` o `estado: "publicada"` sigue creando un borrador; el borrador no aparece en el listado ni en el detalle públicos; la portada web sigue igual.
- Actualiza el `README.md` con ejemplos `curl` (listar, detalle, crear con token) y el paso para obtener el token.

No implementes FastAPI, agentes ni MCP. Resume los cambios y los resultados de las pruebas.
