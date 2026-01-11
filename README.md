# Práctica UT04 - Persistencia de datos

## Información
- **Módulo:** Desarrollo Web en Entorno Servidor
- **Curso:** 2025/2026
- **Alumno:** LuisTejero
- **Fecha:** 03/01/2026

## Objetivos del proyecto 
- Modelar datos complejos utilizando Django ORM. 
- Implementar formularios con validaciones personalizadas. 
- Gestionar roles (alumno/profesor) dentro de la aplicación. 
- Configurar PostgreSQL como motor de base de datos. 
- Aplicar migraciones y mantener la integridad de los datos. 
- Desarrollar vistas funcionales para creación, entrega y validación de tareas. 
--- 

## Decisiones técnicas tomadas 
### 1. Modelo de usuario 
Se ha extendido `AbstractUser` para añadir el campo `role`, que permite distinguir entre alumnos y profesores. 
Esta decisión simplifica la lógica de permisos y facilita la personalización futura del usuario. 

### 2. Modelo de tareas 
El modelo `Task` incluye campos que permiten representar los tres tipos de tareas requeridos: 
- **Individual** 
- **Grupal** 
- **Evaluable** 

Se añadieron campos como: 
- `type` 
- `status` 
- `requires_teacher_validation` 
- `delivery_date` 
- `task_delivery_file` 

Esto permite gestionar todo el ciclo de vida de una tarea. 

### 3. Relaciones entre modelos Se han definido las siguientes relaciones: 
- `creator` → FK a User 
- `members` → ManyToManyField 
- `teacher_validator` → FK opcional 

Estas relaciones permiten representar: 
- quién crea la tarea 
- quién participa 
- quién la valida 

### 4. Formularios y validaciones 
Los formularios incluyen validaciones como: 
- fecha de entrega posterior a la fecha de creación 
- obligatoriedad de archivo en la entrega 
- validación por profesor solo si la tarea lo requiere 

### 5. Vistas y lógica de negocio 
Se han implementado vistas específicas para cada rol: 
- **Alumno**: crear tareas, ver tareas, entregar tareas 
- **Profesor**: validar tareas evaluables 
- **Ambos**: ver perfil, ver listado de usuarios 

### 6. Gestión de roles 
Aunque no se implementa un sistema de permisos avanzado, el rol del usuario controla: 
- qué vistas puede ver 
- qué acciones puede realizar 
- qué tareas puede validar 

### 7. Persistencia con PostgreSQL 
El proyecto utiliza PostgreSQL como base de datos principal. En `settings.py` se configuró: 
- ENGINE: `django.db.backends.postgresql` 
- NAME: `classroom_tasks` 
- USER: `postgres` 
- PASSWORD: configurado localmente 

### 8. Migraciones y datos iniciales 
Se han generado y aplicado todas las migraciones necesarias. El proyecto incluye datos de prueba creados manualmente durante el desarrollo. ### 9. Buenas prácticas de Git El repositorio contiene: 
- commits distribuidos a lo largo del desarrollo 
- mensajes descriptivos 
- estructura clara del proyecto 
- `.gitignore` configurado correctamente 
--- 

##  Estructura del proyecto
classroom_tasks/
├── accounts/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── accounts/
│           ├── list_users.html
│           ├── profile.html
│           └── register.html
│
├── tasks/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── tasks/
│           ├── base.html
│           ├── create_task.html
│           ├── deliver_task.html
│           ├── list_my_tasks.html
│           ├── task_detail.html
│           └── tasks_to_validate.html
│
├── classroom_tasks/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── templates/
│   ├── base.html
│   └── registration/
│       └── login.html
│
├── deliveries/
│
├── manage.py
├── requirements.txt


## Instalación y ejecución

### Requisitos
- Python 3.x  
- Django 5.x  
- PostgreSQL  
- psycopg2  

### Pasos

```bash
git clone <https://github.com/LuisTejero25/DWES-Practica-UT04>
cd classroom_tasks
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver