# 🎯 Job Application Tracker

Sistema de seguimiento de postulaciones laborales diseñado para organizar y monitorear tu búsqueda de empleo de manera eficiente.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Características

- 📊 **Dashboard interactivo** con métricas en tiempo real
- 📝 **CRUD completo** de postulaciones laborales
- 🏷️ **Sistema de estados**: Postulado → En revisión → Entrevista → Oferta → Rechazado/Aceptado
- 🔔 **Seguimientos** con fechas de recordatorio
- 📈 **Métricas detalladas**: tasa de respuesta, tiempo promedio, pipeline de conversión
- 🔍 **Búsqueda y filtros** avanzados
- 📤 **Import/Export** CSV
- 📱 **Diseño responsive** para móvil y desktop
- 🎨 **Interfaz moderna** con tema oscuro

## 🚀 Instalación

### Requisitos

- Python 3.8 o superior
- pip

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/AriGrela-Clawd/job-tracker.git
cd job-tracker
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

4. **Ejecutar la aplicación**
```bash
python main.py
```

5. **Abrir en navegador**
```
http://localhost:8000
```

## 📖 Uso

### Dashboard
El panel principal muestra:
- Total de postulaciones
- Tasa de respuesta
- Postulaciones esta semana/mes
- Pipeline visual de estados
- Seguimientos pendientes

### Agregar Postulación
1. Click en "Nueva" en la navbar
2. Completar los campos:
   - Empresa y puesto (obligatorios)
   - URL de la oferta
   - Estado inicial
   - Fecha de postulación
   - Fecha de seguimiento (para recordatorios)
   - Información adicional (ubicación, modalidad, salario, contacto, notas)
3. Guardar

### Gestionar Estados
- Cambiar estado rápidamente desde el detalle de postulación
- Los estados disponibles son: Postulado, En revisión, Entrevista, Oferta, Rechazado, Aceptado

### Métricas
Visita la sección "Métricas" para ver:
- Pipeline de conversión
- Desglose por estado
- Tasa de entrevistas y ofertas
- Tips para mejorar tu búsqueda

### Exportar Datos
- Desde el dashboard o métricas, click en "Exportar CSV"
- Obtén todos tus datos en formato CSV para análisis externo

## 🏗️ Arquitectura

```
job-tracker/
├── main.py              # FastAPI application
├── database.py          # SQLAlchemy models & operations
├── requirements.txt     # Dependencies
├── README.md           # This file
├── static/
│   ├── css/
│   │   └── style.css   # Stylesheet (tema oscuro)
│   └── js/
│       └── app.js      # Frontend JavaScript
└── templates/          # Jinja2 templates
    ├── base.html
    ├── dashboard.html
    ├── postulaciones.html
    ├── form.html
    ├── detail.html
    └── metricas.html
```

## 🛠️ Stack Tecnológico

- **Backend**: FastAPI (Python)
- **Base de datos**: SQLite con SQLAlchemy ORM
- **Frontend**: Jinja2 Templates + Vanilla JS
- **Estilos**: CSS3 custom (tema oscuro)
- **Iconos**: Font Awesome

## 🔧 Configuración

### Variables de entorno

Crea un archivo `.env` opcional:

```env
DATABASE_URL=sqlite:///data/job_tracker.db
```

### Cambiar puerto

Edita `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Cambia el puerto aquí
```

## 📊 Modelo de Datos

### Postulación
- `id`: Identificador único
- `empresa`: Nombre de la empresa
- `puesto`: Título del puesto
- `url_oferta`: Enlace a la oferta
- `fecha_postulacion`: Fecha de postulación
- `estado`: Estado actual
- `notas`: Notas y seguimiento
- `fecha_seguimiento`: Fecha para recordatorio
- `fecha_respuesta`: Fecha de respuesta recibida
- `tags`: Etiquetas separadas por comas
- `contacto_nombre`: Nombre del reclutador
- `contacto_email`: Email del contacto
- `salario_ofrecido`: Rango salarial
- `ubicacion`: Ubicación del puesto
- `modalidad`: Remoto/Híbrido/Presencial

## 🎯 Tips de Uso

1. **Sé consistente**: Registra cada postulación inmediatamente
2. **Usa seguimientos**: Establece fechas de seguimiento para no olvidar
3. **Agrega notas**: Documenta feedback y detalles importantes
4. **Revisa métricas**: Analiza tu pipeline semanalmente
5. **Exporta backups**: Guarda tus datos regularmente

## 🔮 Roadmap

- [ ] Integración con LinkedIn
- [ ] Notificaciones por email
- [ ] Gráficos interactivos
- [ ] App móvil (PWA)
- [ ] Autenticación de usuarios
- [ ] Múltiples perfiles de búsqueda

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-feature`)
3. Commit tus cambios (`git commit -am 'Agrega nueva feature'`)
4. Push a la rama (`git push origin feature/nueva-feature`)
5. Abre un Pull Request

## 📝 Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.

## 🌟 Creado para

**Ari Grela** - Técnico en audiovisuales y estudiante de programación en búsqueda de nuevas oportunidades laborales.

---

<p align="center">
  <strong>Job Application Tracker</strong> - Organiza tu búsqueda, mejora tus resultados 🎯
</p>
