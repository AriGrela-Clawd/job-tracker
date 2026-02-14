"""
Database models and operations for Job Application Tracker
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/job_tracker.db')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Estado enum values
ESTADOS = ['Postulado', 'En revisión', 'Entrevista', 'Oferta', 'Rechazado', 'Aceptado', 'Sin respuesta']


class Postulacion(Base):
    __tablename__ = 'postulaciones'
    
    id = Column(Integer, primary_key=True, index=True)
    empresa = Column(String(200), nullable=False, index=True)
    puesto = Column(String(200), nullable=False)
    url_oferta = Column(String(500), nullable=True)
    fecha_postulacion = Column(Date, nullable=False, default=datetime.now)
    estado = Column(String(50), nullable=False, default='Postulado')
    notas = Column(Text, nullable=True)
    fecha_seguimiento = Column(Date, nullable=True)
    fecha_respuesta = Column(Date, nullable=True)
    tags = Column(String(300), nullable=True)  # Comma-separated tags
    contacto_nombre = Column(String(150), nullable=True)
    contacto_email = Column(String(150), nullable=True)
    salario_ofrecido = Column(String(50), nullable=True)
    ubicacion = Column(String(150), nullable=True)
    modalidad = Column(String(50), nullable=True)  # Remoto, Híbrido, Presencial
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_postulacion(db, empresa: str, puesto: str, **kwargs) -> Postulacion:
    """Create a new job application"""
    db_postulacion = Postulacion(
        empresa=empresa,
        puesto=puesto,
        **kwargs
    )
    db.add(db_postulacion)
    db.commit()
    db.refresh(db_postulacion)
    return db_postulacion


def get_postulacion(db, postulacion_id: int) -> Optional[Postulacion]:
    """Get a specific job application by ID"""
    return db.query(Postulacion).filter(Postulacion.id == postulacion_id).first()


def get_postulaciones(
    db, 
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    empresa: Optional[str] = None,
    tags: Optional[str] = None,
    search: Optional[str] = None,
    order_by: str = 'fecha_postulacion',
    order_desc: bool = True
) -> List[Postulacion]:
    """Get job applications with filters"""
    query = db.query(Postulacion)
    
    if estado:
        query = query.filter(Postulacion.estado == estado)
    
    if empresa:
        query = query.filter(Postulacion.empresa.ilike(f'%{empresa}%'))
    
    if tags:
        query = query.filter(Postulacion.tags.ilike(f'%{tags}%'))
    
    if search:
        search_filter = (
            Postulacion.empresa.ilike(f'%{search}%') |
            Postulacion.puesto.ilike(f'%{search}%') |
            Postulacion.notas.ilike(f'%{search}%')
        )
        query = query.filter(search_filter)
    
    # Ordering
    if order_desc:
        query = query.order_by(getattr(Postulacion, order_by).desc())
    else:
        query = query.order_by(getattr(Postulacion, order_by))
    
    return query.offset(skip).limit(limit).all()


def update_postulacion(db, postulacion_id: int, **kwargs) -> Optional[Postulacion]:
    """Update a job application"""
    db_postulacion = get_postulacion(db, postulacion_id)
    if not db_postulacion:
        return None
    
    for key, value in kwargs.items():
        if hasattr(db_postulacion, key):
            setattr(db_postulacion, key, value)
    
    db_postulacion.updated_at = datetime.now()
    db.commit()
    db.refresh(db_postulacion)
    return db_postulacion


def delete_postulacion(db, postulacion_id: int) -> bool:
    """Delete a job application"""
    db_postulacion = get_postulacion(db, postulacion_id)
    if not db_postulacion:
        return False
    
    db.delete(db_postulacion)
    db.commit()
    return True


def get_dashboard_stats(db) -> Dict[str, Any]:
    """Get dashboard statistics"""
    total = db.query(Postulacion).count()
    
    # Count by status
    estado_counts = {}
    for estado in ESTADOS:
        count = db.query(Postulacion).filter(Postulacion.estado == estado).count()
        estado_counts[estado] = count
    
    # Response rate (respondidos = no Postulado ni Sin respuesta)
    respondidos = db.query(Postulacion).filter(
        Postulacion.estado.notin_(['Postulado', 'Sin respuesta'])
    ).count()
    tasa_respuesta = (respondidos / total * 100) if total > 0 else 0
    
    # Applications this week
    week_ago = datetime.now().date() - timedelta(days=7)
    esta_semana = db.query(Postulacion).filter(
        Postulacion.fecha_postulacion >= week_ago
    ).count()
    
    # Applications this month
    month_ago = datetime.now().date() - timedelta(days=30)
    este_mes = db.query(Postulacion).filter(
        Postulacion.fecha_postulacion >= month_ago
    ).count()
    
    # Average response time (for applications with fecha_respuesta)
    respuestas = db.query(Postulacion).filter(Postulacion.fecha_respuesta != None).all()
    if respuestas:
        tiempos = [(p.fecha_respuesta - p.fecha_postulacion).days for p in respuestas]
        tiempo_promedio = sum(tiempos) / len(tiempos)
    else:
        tiempo_promedio = 0
    
    # Pending follow-ups (fecha_seguimiento <= today)
    hoy = datetime.now().date()
    seguimientos_pendientes = db.query(Postulacion).filter(
        Postulacion.fecha_seguimiento <= hoy,
        Postulacion.estado.in_(['Postulado', 'En revisión'])
    ).count()
    
    # No response after 14 days (still Postulado)
    dias_sin_respuesta = 14
    limite = hoy - timedelta(days=dias_sin_respuesta)
    sin_respuesta = db.query(Postulacion).filter(
        Postulacion.estado == 'Postulado',
        Postulacion.fecha_postulacion <= limite
    ).count()
    
    return {
        'total': total,
        'estado_counts': estado_counts,
        'tasa_respuesta': round(tasa_respuesta, 1),
        'esta_semana': esta_semana,
        'este_mes': este_mes,
        'tiempo_promedio_respuesta': round(tiempo_promedio, 1),
        'seguimientos_pendientes': seguimientos_pendientes,
        'sin_respuesta_14dias': sin_respuesta,
        'respondidos': respondidos
    }


def get_seguimientos_pendientes(db, dias: int = 7) -> List[Postulacion]:
    """Get job applications needing follow-up"""
    hoy = datetime.now().date()
    limite = hoy + timedelta(days=dias)
    
    return db.query(Postulacion).filter(
        Postulacion.fecha_seguimiento <= limite,
        Postulacion.estado.in_(['Postulado', 'En revisión'])
    ).order_by(Postulacion.fecha_seguimiento).all()


def get_postulaciones_para_exportar(db) -> List[Postulacion]:
    """Get all applications for export"""
    return db.query(Postulacion).order_by(Postulacion.fecha_postulacion.desc()).all()


def bulk_import(db, postulaciones: List[Dict]) -> int:
    """Bulk import job applications from CSV"""
    count = 0
    for p in postulaciones:
        try:
            # Parse dates
            fecha_post = p.get('fecha_postulacion')
            if fecha_post and isinstance(fecha_post, str):
                fecha_post = datetime.strptime(fecha_post, '%Y-%m-%d').date()
            
            fecha_seg = p.get('fecha_seguimiento')
            if fecha_seg and isinstance(fecha_seg, str):
                fecha_seg = datetime.strptime(fecha_seg, '%Y-%m-%d').date()
            
            fecha_resp = p.get('fecha_respuesta')
            if fecha_resp and isinstance(fecha_resp, str):
                fecha_resp = datetime.strptime(fecha_resp, '%Y-%m-%d').date()
            
            postulacion = Postulacion(
                empresa=p.get('empresa', 'Sin empresa'),
                puesto=p.get('puesto', 'Sin puesto'),
                url_oferta=p.get('url_oferta'),
                fecha_postulacion=fecha_post or datetime.now().date(),
                estado=p.get('estado', 'Postulado'),
                notas=p.get('notas'),
                fecha_seguimiento=fecha_seg,
                fecha_respuesta=fecha_resp,
                tags=p.get('tags'),
                contacto_nombre=p.get('contacto_nombre'),
                contacto_email=p.get('contacto_email'),
                salario_ofrecido=p.get('salario_ofrecido'),
                ubicacion=p.get('ubicacion'),
                modalidad=p.get('modalidad')
            )
            db.add(postulacion)
            count += 1
        except Exception as e:
            print(f"Error importing row: {e}")
            continue
    
    db.commit()
    return count
