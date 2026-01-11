# Pr-ctica-UT04-Persistencia-de-adtos
🛠 Decisiones Técnicas y Arquitectura del Proyecto
En el desarrollo de esta plataforma de gestión educativa, he priorizado la creación de un sistema modular y escalable. A continuación, detallo las decisiones técnicas clave:

1. Extensión del Modelo de Usuario y Control de Acceso
Para gestionar la seguridad, decidí no depender únicamente de los grupos de Django. En su lugar, extendí el modelo AbstractUser para incluir un campo de Rol personalizado en la base de datos PostgreSQL.

Impacto: Esto me permitió centralizar la lógica de permisos. Implementé una vista "Portero" (root_redirect) que funciona como un despachador: analiza el rol del usuario autenticado en tiempo real y gestiona la redirección hacia el Panel de Alumno o el Panel de Profesor, evitando accesos no autorizados a rutas administrativas.

2. Modelado de Tareas mediante Herencia
En lugar de crear tablas independientes, utilicé herencia de modelos.

Decisión: El modelo base Tarea encapsula la lógica de validación (el campo requiere_evaluacion), mientras que las clases hijas gestionan las relaciones específicas (individuos o grupos de alumnos). Esto facilita que el motor de filtrado en las vistas pueda recuperar tareas de forma eficiente mediante consultas Q complejas en el ORM de Django.

3. Frontend Desacoplado y UX
Para asegurar que la interfaz fuera "agradable" y no solo funcional, tomé dos decisiones de diseño:

CSS Externo: Decidí extraer todos los estilos a un archivo style.css independiente. Esto permite que el mantenimiento visual sea independiente de la lógica de las plantillas.

Widgets Personalizados: En los formularios de creación de tareas, sobrescribí los widgets por defecto para integrar el tipo datetime-local y clases de control de formularios. Esto garantiza que el usuario interactúe con calendarios nativos del navegador en lugar de introducir fechas en texto plano.

4. Flujo de Trabajo y Seguridad de Sesiones
Gestión de Sesiones: Configuré el sistema para que el ciclo de vida de la sesión sea estricto. Mediante las constantes de configuración en settings.py, aseguré que tanto el login como el logout redirijan siempre a puntos controlados, manteniendo al usuario dentro del flujo de la aplicación sin posibilidad de "quedarse colgado" en páginas de perfil genéricas.

Validación en Servidor: La lógica de "Finalizar Tarea" se ejecuta exclusivamente en el servidor. Aunque un alumno intente marcar una tarea como completada, el código verifica si requiere evaluación; si es así, el estado no cambia hasta que un usuario con rol de profesor ejecuta la acción, manteniendo la integridad del flujo académico.

Todos los commits son del mismo dia ya que he hecho todo hoy. (6 horas aprox.)
