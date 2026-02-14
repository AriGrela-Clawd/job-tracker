# 🎯 Job Application Tracker

> Sistema de seguimiento de postulaciones laborales diseñado para organizar y optimizar tu búsqueda de empleo.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Características

### 📋 Gestión de Postulaciones
- **CRUD completo**: Crear, leer, actualizar y eliminar postulaciones
- **Campos detallados**: Empresa, puesto, URL, fechas, contactos, salario, ubicación
- **Estados del pipeline**: Postulado → En revisión → Entrevista → Oferta → Rechazado/Aceptado
- **Sistema de tags**: Categoriza tus postulaciones
- **Notas**: Registra feedback y detalles importantes

### 📊 Dashboard y Métricas
- **Resumen visual**: Total de postulaciones, tasa de respuesta, actividad reciente
- **Pipeline visual**: Ver tu progreso en cada etapa
- **Métricas detalladas**:
  - Total de postulaciones
  - Tasa de respuesta (%)
  - Postulaciones esta semana/mes
  - Tiempo promedio de respuesta
  - Postulaciones sin respuesta >14 días
- **Seguimientos pendientes**: Alertas de recordatorios

### 🔍 Filtros y Búsqueda
- Buscar por empresa, puesto o notas
- Filtrar por estado
- Filtrar por empresa específica
- Paginación de resultados

### 📁 Import/Export
- **Exportar a CSV**: Backup de todas tus postulaciones
- **Importar desde CSV**: Carga masiva de datos

### 💻 Interfaz de Usuario
- **Diseño moderno**: Interfaz limpia y profesional
- **Responsive**: Funciona en desktop, tablet y móvil
- **Tema claro**: Colores agradables y buen contraste
- **Navegación intuitiva**: Menú claro y accesible

---

## 🚀 Instalación

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar o descargar el proyecto**
```bash
cd ~/clawd/proyectos/job-tracker
```

2. **Crear entorno virtual (opcional pero recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Iniciar la aplicación**
```bash
python main.py
```

5. **Abrir en el navegador**
```
http://localhost:8000
```

---

## 📖 Guía de Uso

### Crear una Nueva Postulación

1. Haz clic en **"Nueva Postulación"** en el menú o en el botón verde del dashboard
2. Completa los campos obligatorios:
   - **Empresa**: Nombre de la empresa
   - **Puesto**: Título del puesto
   - **Fecha de postulación**: Cuando enviaste tu aplicación
3. Agrega información adicional opcional:
   - URL de la oferta
   - Estado actual
   - Fecha de seguimiento (para recordatorios)
   - Ubicación y modalidad
   - Datos de contacto del reclutador
   - Tags para categorizar
   - Notas

### Actualizar el Estado

1. Ve a la lista de postulaciones o al detalle de una postulación
2. Usa los botones de estado rápido o edita la postulación
3. Los estados disponibles son:
   - **Postulado**: Acabas de enviar tu CV
   - **En revisión**: La empresa está revisando tu perfil
   - **Entrevista**: Tienes una entrevista programada
   - **Oferta**: Te hicieron una oferta
   - **Rechazado**: No fueron seleccionados
   - **Aceptado**: ¡Conseguiste el trabajo!

### Seguimientos y Recordatorios

1. Al crear/editar una postulación, establece una **"Fecha de seguimiento"**
2. El dashboard mostrará alertas cuando sea necesario hacer seguimiento
3. Las postulaciones sin respuesta después de 14 días aparecen destacadas

### Exportar tus Datos

1. Ve a **"Métricas"** en el menú
2. Haz clic en **"Exportar Datos"**
3. Se descargará un archivo CSV con todas tus postulaciones

### Importar Datos

1. Prepara un archivo CSV con las columnas correspondientes
2. Usa la función de importación (API disponible)

---

## 🗂️ Estructura del Proyecto

```
job-tracker/
├── main.py              # Aplicación FastAPI principal
├── database.py          # Modelos y operaciones de base de datos
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Este archivo
├── data/               # Base de datos SQLite (se crea automáticamente)
├── templates/          # Plantillas HTML Jinja2
│   ├── base.html       # Plantilla base
│   ├── dashboard.html  # Panel principal
│   ├── postulaciones.html  # Lista de postulaciones
│   ├── form.html       # Formulario crear/editar
│   ├── detail.html     # Detalle de postulación
│   └── metricas.html   # Métricas detalladas
└── static/             # Archivos estáticos
    ├── css/
    │   └── style.css   # Estilos CSS
    └── js/
        └── app.js      # JavaScript principal
```

---

## 🔧 API Endpoints

La aplicación expone los siguientes endpoints:

### Web Interface
- `GET /` - Dashboard principal
- `GET /postulaciones` - Lista de postulaciones
- `GET /postulaciones/nueva` - Formulario de creación
- `GET /postulaciones/{id}` - Detalle de postulación
- `GET /postulaciones/{id}/editar` - Formulario de edición
- `GET /metricas` - Métricas detalladas

### API JSON
- `GET /api/stats` - Estadísticas del dashboard
- `GET /api/seguimientos` - Seguimientos pendientes

### Data Operations
- `GET /exportar/csv` - Exportar todas las postulaciones a CSV
- `POST /importar/csv` - Importar postulaciones desde CSV

---

## 💡 Tips para Maximizar el Uso

### 1. Sé Consistente
- Registra cada postulación inmediatamente después de enviarla
- Actualiza los estados regularmente
- Usa las fechas de seguimiento para no perder oportunidades

### 2. Usa Tags Efectivamente
- Tags como: `remoto`, `senior`, `fintech`, `startup`
- Te permitirán filtrar y analizar por categorías

### 3. Analiza tus Métricas
- Revisa regularmente tu tasa de respuesta
- Identifica en qué etapa del pipeline te quedas
- Ajusta tu estrategia basado en los datos

### 4. Haz Seguimiento Proactivo
- Establece fechas de seguimiento 7-10 días después de postularte
- Si no hay respuesta en 14 días, considera enviar un email de seguimiento

---

## 🛠️ Desarrollo

### Variables de Entorno

Puedes configurar las siguientes variables:

```bash
# Base de datos (opcional, por defecto SQLite local)
DATABASE_URL=sqlite:///data/job_tracker.db

# Puerto (opcional, por defecto 8000)
PORT=8000
```

### Ejecutar en modo desarrollo

```bash
# Con recarga automática
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🤝 Contribuir

Este es un proyecto personal para Ari, pero las sugerencias son bienvenidas.

---

## 📄 Licencia

MIT License - Libre para usar y modificar.

---

## 🙏 Créditos

Creado con ❤️ para Ari Grela como herramienta para optimizar su búsqueda laboral.

**Stack tecnológico:**
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para Python
- [Jinja2](https://jinja.palletsprojects.com/) - Templating engine
- [Inter](https://fonts.google.com/specimen/Inter) - Tipografía
- [Font Awesome](https://fontawesome.com/) - Iconos

---

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias:
1. Revisa este README
2. Verifica que cumples con todos los requisitos
3. Revisa los logs en la consola

---

**¡Éxito en tu búsqueda laboral! 🚀**
