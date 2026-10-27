# Briefing — Blog de Cocina

## 1. Resumen
Un blog de cocina muy básico donde cualquier persona puede **publicar recetas** y **ver las recetas** que publican otros. Está pensado para cocineros caseros que quieren compartir lo que preparan y para quienes buscan ideas para cocinar. Su seña de identidad es un estilo **minimalista y simple**: solo publicar y leer, sin nada más.

## 2. Problema / motivación
- **Qué resuelve**
  - Compartir una receta casera hoy exige usar plataformas que no están pensadas para ello o que están sobrecargadas.
  - Leer una receta en internet suele implicar anuncios, ventanas emergentes, historias personales larguísimas y comentarios antes de llegar a los ingredientes.
- **Cómo se resuelve hoy**
  - **Redes sociales (Instagram, Facebook, TikTok):** la receta queda enterrada entre fotos, vídeos y comentarios; el texto es difícil de seguir mientras se cocina.
  - **Grupos de mensajería (WhatsApp):** la receta se pierde en el chat y solo la ve un grupo cerrado.
  - **Webs de recetas grandes:** obligan a registrarse para publicar y las páginas están saturadas de publicidad.
  - **Blog propio (WordPress, Blogger):** requiere configurar y mantener un sitio entero solo para compartir unas pocas recetas.
- **Motivación**
  - Crear un espacio limpio donde la receta sea lo único importante y publicar lleve un minuto.

## 3. Usuarios objetivo
- **Autor — cocinero casero**
  - Cocina en casa y quiere compartir sus recetas con otras personas.
  - Necesita publicar rápido, sin crear cuenta ni aprender a usar una herramienta compleja.
- **Lector — persona que busca qué cocinar**
  - Busca ideas para cocinar, muchas veces desde el móvil y en la propia cocina.
  - Necesita ver los ingredientes y los pasos de forma clara, sin distracciones.

## 4. Objetivos
- **OBJ-1:** Que cualquier persona pueda publicar una receta en menos de 2 minutos.
- **OBJ-2:** Que cualquier visitante pueda ver todas las recetas publicadas y leer el detalle de cada una.
- **OBJ-3:** Ofrecer una lectura cómoda y sin distracciones, en móvil y escritorio.
- **OBJ-4:** Tener una primera versión funcional (MVP) terminada dentro del plazo de la clase.

## 5. Ideas de funcionalidades (en bruto, sin priorizar)
- Formulario para publicar una receta.
- Título, ingredientes y pasos de la receta.
- Nombre del autor.
- Descripción corta de la receta.
- Foto de la receta.
- Listado de todas las recetas en la página principal.
- Página de detalle de cada receta.
- Ingredientes en lista y pasos numerados.
- Fecha de publicación.
- Tiempo de preparación y número de raciones.
- Editar y borrar recetas.
- Cuentas de usuario y perfil del autor.
- Categorías (postres, entrantes, platos principales…).
- Buscador de recetas.
- Me gusta y comentarios.
- Guardar recetas favoritas.
- Botón de imprimir receta.
- Modo oscuro.

## 6. Restricciones
- **Stack:** Python + Django (plantillas de Django renderizadas en el servidor) + SQLite + CSS propio.
- **Presupuesto:** 0 €; solo herramientas y servicios gratuitos.
- **Plazos:** los del calendario de la clase; la v1 debe caber en ese periodo.
- **Herramientas:** VS Code, Git, Python con entorno virtual (`venv`), `pip` y un navegador moderno.
- **Equipo:** desarrollo individual o en grupo reducido (proyecto de clase).

## 7. Referencias
- **Cookpad**
  - Me gusta: cualquiera puede publicar recetas caseras; el formato de ingredientes + pasos es claro.
  - No me gusta: exige registro y tiene muchas funciones sociales que añaden ruido.
- **Allrecipes / RecetasGratis**
  - Me gusta: gran variedad de recetas y estructura de receta estandarizada.
  - No me gusta: publicidad abundante, páginas pesadas y lentas.
- **Blogs de cocina personales (WordPress)**
  - Me gusta: el autor tiene su espacio propio.
  - No me gusta: largas introducciones antes de la receta; montar uno es costoso.
- **Instagram**
  - Me gusta: lo visual y lo fácil que es compartir.
  - No me gusta: la receta queda escondida en la descripción y es incómoda de seguir.
- **Blogs minimalistas tipo Bear Blog**
  - Me gusta: diseño extremadamente limpio, carga instantánea, la tipografía como protagonista.
  - No me gusta: no están pensados para recetas (sin estructura de ingredientes y pasos).

## 8. Fuera de alcance (primera idea)
- Me gusta / reacciones.
- Comentarios.
- Seguidores y perfiles sociales.
- Publicidad.
- Cualquier funcionalidad que no sea publicar o visualizar recetas.

## 9. Dudas abiertas
- ¿Dónde se desplegará la aplicación (solo en local o en un servidor público como PythonAnywhere)?
- ¿Se incluye la foto de la receta en la v1 o se deja para después?
- Sin login, ¿basta con el panel de administración de Django (solo para el responsable del blog) para borrar recetas inapropiadas o con errores?
- ¿Se añaden tiempo de preparación y raciones como campos de la receta?
- ¿Se ofrece una API REST (Django REST Framework) para que otros programas lean las recetas publicadas y creen borradores? Evaluada con [vision.md](spec/vision.md): no cambia la web ni añade ruido para el lector, y reutiliza el modelo `Receta`. Aprobada como opcional (RF-14).
