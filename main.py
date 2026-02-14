"""
Job Application Tracker - FastAPI Application
"""
from fastapi import FastAPI, Request, Depends, Form, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, date
import csv
import io
from pathlib import Path

from database import (
    get_db, create_postulacion, get_postulacion, get_postulaciones,
    update_postulacion, delete_postulacion, get_dashboard_stats,
    get_seguimientos_pendientes, get_postulaciones_para_exportar,
    bulk_import, ESTADOS, Postulacion
)

# Create FastAPI app
app = FastAPI(
    title="Job Application Tracker",
    description="Sistema de seguimiento de postulaciones laborales",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Ensure data directory exists
Path("data").mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Main dashboard page"""
    stats = get_dashboard_stats(db)
    seguimientos = get_seguimientos_pendientes(db, dias=7)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": stats,
        "seguimientos": seguimientos,
        "estados": ESTADOS
    })


@app.get("/postulaciones", response_class=HTMLResponse)
async def list_postulaciones(
    request: Request,
    page: int = Query(1, ge=1),
    estado: Optional[str] = None,
    empresa: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all job applications with pagination and filters"""
    per_page = 20
    skip = (page - 1) * per_page
    
    postulaciones = get_postulaciones(
        db, skip=skip, limit=per_page,
        estado=estado, empresa=empresa, search=search,
        order_by='fecha_postulacion', order_desc=True
    )
    
    # Get total count for pagination
    total = len(get_postulaciones(db, estado=estado, empresa=empresa, search=search))
    total_pages = (total + per_page - 1) // per_page
    
    return templates.TemplateResponse("postulaciones.html", {
        "request": request,
        "postulaciones": postulaciones,
        "page": page,
        "total_pages": total_pages,
        "total": total,
        "estado_filter": estado,
        "empresa_filter": empresa,
        "search": search,
        "estados": ESTADOS
    })


@app.get("/postulaciones/nueva", response_class=HTMLResponse)
async def new_postulacion_form(request: Request):
    """Form to create new job application"""
    return templates.TemplateResponse("form.html", {
        "request": request,
        "postulacion": None,
        "estados": ESTADOS,
        "titulo": "Nueva Postulación"
    })


@app.post("/postulaciones/nueva")
async def create_postulacion_handler(
    empresa: str = Form(...),
    puesto: str = Form(...),
    url_oferta: Optional[str] = Form(None),
    fecha_postulacion: str = Form(...),
    estado: str = Form(...),
    notas: Optional[str] = Form(None),
    fecha_seguimiento: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    contacto_nombre: Optional[str] = Form(None),
    contacto_email: Optional[str] = Form(None),
    salario_ofrecido: Optional[str] = Form(None),
    ubicacion: Optional[str] = Form(None),
    modalidad: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Create new job application"""
    try:
        fecha_post = datetime.strptime(fecha_postulacion, '%Y-%m-%d').date()
        fecha_seg = datetime.strptime(fecha_seguimiento, '%Y-%m-%d').date() if fecha_seguimiento else None
        
        create_postulacion(
            db,
            empresa=empresa,
            puesto=puesto,
            url_oferta=url_oferta,
            fecha_postulacion=fecha_post,
            estado=estado,
            notas=notas,
            fecha_seguimiento=fecha_seg,
            tags=tags,
            contacto_nombre=contacto_nombre,
            contacto_email=contacto_email,
            salario_ofrecido=salario_ofrecido,
            ubicacion=ubicacion,
            modalidad=modalidad
        )
        return RedirectResponse(url="/postulaciones", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating postulacion: {str(e)}")


@app.get("/postulaciones/{postulacion_id}", response_class=HTMLResponse)
async def view_postulacion(
    request: Request,
    postulacion_id: int,
    db: Session = Depends(get_db)
):
    """View job application details"""
    postulacion = get_postulacion(db, postulacion_id)
    if not postulacion:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    
    return templates.TemplateResponse("detail.html", {
        "request": request,
        "postulacion": postulacion,
        "estados": ESTADOS
    })


@app.get("/postulaciones/{postulacion_id}/editar", response_class=HTMLResponse)
async def edit_postulacion_form(
    request: Request,
    postulacion_id: int,
    db: Session = Depends(get_db)
):
    """Form to edit job application"""
    postulacion = get_postulacion(db, postulacion_id)
    if not postulacion:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    
    return templates.TemplateResponse("form.html", {
        "request": request,
        "postulacion": postulacion,
        "estados": ESTADOS,
        "titulo": "Editar Postulación"
    })


@app.post("/postulaciones/{postulacion_id}/editar")
async def update_postulacion_handler(
    postulacion_id: int,
    empresa: str = Form(...),
    puesto: str = Form(...),
    url_oferta: Optional[str] = Form(None),
    fecha_postulacion: str = Form(...),
    estado: str = Form(...),
    notas: Optional[str] = Form(None),
    fecha_seguimiento: Optional[str] = Form(None),
    fecha_respuesta: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    contacto_nombre: Optional[str] = Form(None),
    contacto_email: Optional[str] = Form(None),
    salario_ofrecido: Optional[str] = Form(None),
    ubicacion: Optional[str] = Form(None),
    modalidad: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Update job application"""
    try:
        fecha_post = datetime.strptime(fecha_postulacion, '%Y-%m-%d').date()
        fecha_seg = datetime.strptime(fecha_seguimiento, '%Y-%m-%d').date() if fecha_seguimiento else None
        fecha_resp = datetime.strptime(fecha_respuesta, '%Y-%m-%d').date() if fecha_respuesta else None
        
        postulacion = update_postulacion(
            db,
            postulacion_id=postulacion_id,
            empresa=empresa,
            puesto=puesto,
            url_oferta=url_oferta,
            fecha_postulacion=fecha_post,
            estado=estado,
            notas=notas,
            fecha_seguimiento=fecha_seg,
            fecha_respuesta=fecha_resp,
            tags=tags,
            contacto_nombre=contacto_nombre,
            contacto_email=contacto_email,
            salario_ofrecido=salario_ofrecido,
            ubicacion=ubicacion,
            modalidad=modalidad
        )
        
        if not postulacion:
            raise HTTPException(status_code=404, detail="Postulación no encontrada")
        
        return RedirectResponse(url=f"/postulaciones/{postulacion_id}", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating postulacion: {str(e)}")


@app.post("/postulaciones/{postulacion_id}/eliminar")
async def delete_postulacion_handler(
    postulacion_id: int,
    db: Session = Depends(get_db)
):
    """Delete job application"""
    success = delete_postulacion(db, postulacion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    return RedirectResponse(url="/postulaciones", status_code=303)


@app.post("/postulaciones/{postulacion_id}/cambiar-estado")
async def cambiar_estado(
    postulacion_id: int,
    nuevo_estado: str = Form(...),
    db: Session = Depends(get_db)
):
    """Quick status change"""
    kwargs = {"estado": nuevo_estado}
    
    # If changing to Rechazado or Aceptado, set fecha_respuesta
    if nuevo_estado in ['Rechazado', 'Aceptado']:
        kwargs["fecha_respuesta"] = date.today()
    
    postulacion = update_postulacion(db, postulacion_id, **kwargs)
    if not postulacion:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    
    return RedirectResponse(url=f"/postulaciones/{postulacion_id}", status_code=303)


# API Endpoints
@app.get("/api/stats")
async def api_stats(db: Session = Depends(get_db)):
    """API endpoint for dashboard stats"""
    return get_dashboard_stats(db)


@app.get("/api/seguimientos")
async def api_seguimientos(
    dias: int = Query(7, ge=1),
    db: Session = Depends(get_db)
):
    """API endpoint for pending follow-ups"""
    seguimientos = get_seguimientos_pendientes(db, dias)
    return {
        "count": len(seguimientos),
        "items": [
            {
                "id": s.id,
                "empresa": s.empresa,
                "puesto": s.puesto,
                "fecha_seguimiento": s.fecha_seguimiento.isoformat() if s.fecha_seguimiento else None,
                "estado": s.estado
            }
            for s in seguimientos
        ]
    }


# Export/Import
@app.get("/exportar/csv")
async def export_csv(db: Session = Depends(get_db)):
    """Export all job applications to CSV"""
    postulaciones = get_postulaciones_para_exportar(db)
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        'id', 'empresa', 'puesto', 'url_oferta', 'fecha_postulacion',
        'estado', 'notas', 'fecha_seguimiento', 'fecha_respuesta', 'tags',
        'contacto_nombre', 'contacto_email', 'salario_ofrecido',
        'ubicacion', 'modalidad'
    ])
    
    # Data
    for p in postulaciones:
        writer.writerow([
            p.id, p.empresa, p.puesto, p.url_oferta,
            p.fecha_postulacion.isoformat() if p.fecha_postulacion else '',
            p.estado, p.notas,
            p.fecha_seguimiento.isoformat() if p.fecha_seguimiento else '',
            p.fecha_respuesta.isoformat() if p.fecha_respuesta else '',
            p.tags, p.contacto_nombre, p.contacto_email,
            p.salario_ofrecido, p.ubicacion, p.modalidad
        ])
    
    output.seek(0)
    
    return FileResponse(
        path=None,
        media_type="text/csv",
        filename=f"postulaciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )


@app.post("/importar/csv")
async def import_csv(
    file_content: str = Form(...),
    db: Session = Depends(get_db)
):
    """Import job applications from CSV"""
    try:
        reader = csv.DictReader(io.StringIO(file_content))
        postulaciones = list(reader)
        count = bulk_import(db, postulaciones)
        return JSONResponse({
            "success": True,
            "imported": count,
            "message": f"Se importaron {count} postulaciones exitosamente"
        })
    except Exception as e:
        return JSONResponse(
            {"success": False, "error": str(e)},
            status_code=400
        )


@app.get("/metricas", response_class=HTMLResponse)
async def metricas_detalladas(request: Request, db: Session = Depends(get_db)):
    """Detailed metrics page"""
    stats = get_dashboard_stats(db)
    
    # Get applications by week for chart
    db_postulaciones = get_postulaciones(db, limit=1000)
    
    return templates.TemplateResponse("metricas.html", {
        "request": request,
        "stats": stats,
        "estados": ESTADOS
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
