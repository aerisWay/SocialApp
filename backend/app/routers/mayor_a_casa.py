# ============================================================
# routers/mayor_a_casa.py — Endpoints del servicio Major a Casa
# ============================================================

from io import BytesIO
from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.caso_mayor_a_casa import CasoMayorACasa
from app.models.comision_mayor_a_casa import ComisionMayorACasa
from app.models.factura_mayor_a_casa import FacturaMayorACasa
from app.schemas.caso_mayor_a_casa import CasoCreate, CasoUpdate, CasoResponse
from app.schemas.comision_mayor_a_casa import ComisionCreate, ComisionUpdate, ComisionResponse
from app.schemas.factura_mayor_a_casa import FacturaUpsert, FacturaResponse
from app.utils.auth import get_current_dept

router = APIRouter(dependencies=[Depends(get_current_dept)])

STATIC_IMG   = Path(__file__).parent.parent / "static" / "img"
UPLOAD_DIR   = Path(__file__).parent.parent / "static" / "uploads" / "facturas"


# ── Localización PDF ───────────────────────────────────────────
PDF_I18N = {
    "es": {
        "activos":    "Informe de Casos Activos",
        "renovacion": "Renovaciones",
        "generated":  "Generado el",
        "total":      "Total",
        "casos":      "casos",
        "hombres":    "Hombres",
        "mujeres":    "Mujeres",
        "no_def":     "No especificado",
        "headers":    ["Apellidos", "Nombre", "DNI", "SIP", "Zona", "Edad", "Sexo", "Teléfono", "Mes Renov.", "F. Alta", "Dirección"],
        "footer":     "Concejalía de Bienestar Social — Ayto. Benidorm",
        "menor_60":   "< 60",
        "60_65":      "60-65",
        "mayor_65":   "> 65",
    },
    "val": {
        "activos":    "Informe de Casos Actius",
        "renovacion": "Renovacions",
        "generated":  "Generat el",
        "total":      "Total",
        "casos":      "casos",
        "hombres":    "Homes",
        "mujeres":    "Dones",
        "no_def":     "No especificat",
        "headers":    ["Cognoms", "Nom", "DNI", "SIP", "Zona", "Edat", "Sexe", "Telèfon", "Mes Renov.", "F. Alta", "Adreça"],
        "footer":     "Regidoria de Benestar Social — Ajunt. Benidorm",
        "menor_60":   "< 60",
        "60_65":      "60-65",
        "mayor_65":   "> 65",
    }
}

_MESES_ES  = ["enero","febrero","marzo","abril","mayo","junio",
              "julio","agosto","septiembre","octubre","noviembre","diciembre"]
_MESES_VAL = ["gener","febrer","març","abril","maig","juny",
              "juliol","agost","setembre","octubre","novembre","desembre"]


# ── Helper: generar PDF ────────────────────────────────────────
def _build_pdf(casos: list, titulo_key: str = "activos", lang: str = "es", extra_titulo: str = "") -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle,
        Paragraph, Spacer, HRFlowable,
    )

    t = PDF_I18N.get(lang, PDF_I18N["es"])
    titulo_full = f"Major a Casa — {t.get(titulo_key, titulo_key)}{extra_titulo}"

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=1.5 * cm, leftMargin=1.5 * cm,
        topMargin=2.2 * cm,   bottomMargin=2.5 * cm,
    )
    styles = getSampleStyleSheet()
    azul  = colors.HexColor("#1f6feb")
    gris  = colors.HexColor("#6e7681")
    claro = colors.HexColor("#f6f8fa")

    title_st = ParagraphStyle("title", parent=styles["Heading1"],
        fontSize=18, textColor=azul, spaceAfter=4, alignment=TA_CENTER)
    sub_st   = ParagraphStyle("sub", parent=styles["Normal"],
        fontSize=10, textColor=gris, spaceAfter=16, alignment=TA_CENTER)
    stats_st = ParagraphStyle("stats", parent=styles["Normal"],
        fontSize=9, textColor=azul, spaceAfter=10, alignment=TA_CENTER)
    cell_st  = ParagraphStyle("cell", parent=styles["Normal"], fontSize=8)

    hombres = sum(1 for c in casos if c.sexo == "hombre")
    mujeres = sum(1 for c in casos if c.sexo == "mujer")
    no_def  = len(casos) - hombres - mujeres

    story = [
        Paragraph(titulo_full, title_st),
        Paragraph(
            f"{t['generated']} {date.today().strftime('%d/%m/%Y')} · "
            f"{t['total']}: {len(casos)} {t['casos']}",
            sub_st,
        ),
        Paragraph(
            f"{t['hombres']}: <b>{hombres}</b>   ·   {t['mujeres']}: <b>{mujeres}</b>"
            + (f"   ·   {t['no_def']}: <b>{no_def}</b>" if no_def > 0 else ""),
            stats_st,
        ),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e1e4e8")),
        Spacer(1, 0.4 * cm),
    ]

    def fmt_date(d): return d.strftime("%d/%m/%Y") if d else "—"
    def fmt_mes(m):  return m if m else "—"
    def fmt_zona(z): return f"Zona {z}" if z else "—"
    def fmt_edad(e): return t.get(e, "—") if e else "—"
    def fmt_sexo(s):
        return {"hombre": "Hombre", "mujer": "Mujer", "no_define": "No define"}.get(s or "", "—")

    headers = t["headers"]
    # 11 columns: apellidos, nombre, dni, sip, zona, edad, sexo, telefono, mes_renov, f_alta, direccion
    col_widths = [3*cm, 2.2*cm, 2.2*cm, 1.8*cm, 1.2*cm, 1.4*cm, 1.5*cm, 2.2*cm, 1.8*cm, 1.8*cm, None]

    data = [headers] + [
        [
            Paragraph(c.apellidos, cell_st),
            Paragraph(c.nombre, cell_st),
            c.dni or "—",
            c.sip or "—",
            fmt_zona(c.zona),
            fmt_edad(c.rango_edad),
            fmt_sexo(c.sexo),
            c.telefono or "—",
            fmt_mes(c.mes_renovacion),
            fmt_date(c.fecha_alta),
            Paragraph(c.direccion or "—", cell_st),
        ]
        for c in casos
    ]

    tabla = Table(data, colWidths=col_widths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), azul),
        ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING",    (0, 0), (-1, 0), 8),
        ("FONTSIZE",      (0, 1), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.white, claro]),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#d0d7de")),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING",       (0, 1), (-1, -1), 5),
        ("ALIGN",         (4, 0), (4, -1), "CENTER"),
    ]))
    story.append(tabla)

    # ── Footer: texto izquierda + logos derecha ────────────────
    main_logo   = STATIC_IMG / "MainLogo.png"
    second_logo = STATIC_IMG / "SecondLogo.png"

    def footer(canvas, _doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(gris)
        canvas.drawString(1.5 * cm, 1.0 * cm, t["footer"])

        page_w  = landscape(A4)[0]
        x_right = page_w - 1.5 * cm

        # SecondLogo — al doble del tamaño anterior (antes: 4cm ancho)
        if second_logo.exists():
            try:
                canvas.drawImage(
                    str(second_logo), x_right - 8.5 * cm, 0.3 * cm,
                    width=8 * cm, height=3.2 * cm,
                    preserveAspectRatio=True, mask='auto',
                )
                x_right -= 8.8 * cm
            except Exception:
                pass

        # MainLogo — a la mitad del tamaño anterior (antes: 1cm ancho)
        if main_logo.exists():
            try:
                canvas.drawImage(
                    str(main_logo), x_right - 0.6 * cm, 0.8 * cm,
                    width=0.5 * cm, height=0.2 * cm,
                    preserveAspectRatio=True, mask='auto',
                )
            except Exception:
                pass

        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return buffer.getvalue()


# ═══════════════════════════════════════════════════════════════
#  ENDPOINTS — CASOS (Usuarios)
# ═══════════════════════════════════════════════════════════════

@router.get("/casos/", response_model=List[CasoResponse], summary="Listar todos los casos")
def list_casos(
    solo_activos: bool = False,
    zona: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(CasoMayorACasa)
    if solo_activos:
        q = q.filter(CasoMayorACasa.activo == True)  # noqa: E712
    if zona:
        q = q.filter(CasoMayorACasa.zona == zona)
    return q.order_by(CasoMayorACasa.apellidos).all()


@router.get("/casos/{caso_id}", response_model=CasoResponse, summary="Obtener un caso por ID")
def get_caso(caso_id: int, db: Session = Depends(get_db)):
    caso = db.query(CasoMayorACasa).filter(CasoMayorACasa.id == caso_id).first()
    if not caso:
        raise HTTPException(status_code=404, detail=f"Caso {caso_id} no encontrado")
    return caso


@router.post("/casos/", response_model=CasoResponse, status_code=201, summary="Crear un nuevo caso")
def create_caso(data: CasoCreate, db: Session = Depends(get_db)):
    if data.dni:
        if db.query(CasoMayorACasa).filter(CasoMayorACasa.dni == data.dni).first():
            raise HTTPException(status_code=400, detail="Ya existe un caso con ese DNI")
    if data.sip:
        if db.query(CasoMayorACasa).filter(CasoMayorACasa.sip == data.sip).first():
            raise HTTPException(status_code=400, detail="Ya existe un caso con ese SIP")
    caso = CasoMayorACasa(**data.model_dump())
    db.add(caso)
    db.commit()
    db.refresh(caso)
    return caso


@router.patch("/casos/{caso_id}", response_model=CasoResponse, summary="Actualizar un caso")
def update_caso(caso_id: int, data: CasoUpdate, db: Session = Depends(get_db)):
    caso = db.query(CasoMayorACasa).filter(CasoMayorACasa.id == caso_id).first()
    if not caso:
        raise HTTPException(status_code=404, detail=f"Caso {caso_id} no encontrado")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(caso, field, value)
    db.commit()
    db.refresh(caso)
    return caso


@router.delete("/casos/{caso_id}", status_code=204, summary="Eliminar un caso")
def delete_caso(caso_id: int, db: Session = Depends(get_db)):
    caso = db.query(CasoMayorACasa).filter(CasoMayorACasa.id == caso_id).first()
    if not caso:
        raise HTTPException(status_code=404, detail=f"Caso {caso_id} no encontrado")
    db.delete(caso)
    db.commit()


@router.get("/casos/informe/pdf", summary="Informe PDF de casos activos")
def generar_informe_pdf(zona: Optional[int] = None, lang: str = "es", db: Session = Depends(get_db)):
    q = db.query(CasoMayorACasa).filter(CasoMayorACasa.activo == True)  # noqa: E712
    extra = f" — Zona {zona}" if zona else ""
    if zona:
        q = q.filter(CasoMayorACasa.zona == zona)
    casos = q.order_by(CasoMayorACasa.apellidos).all()
    pdf_bytes = _build_pdf(casos, titulo_key="activos", lang=lang, extra_titulo=extra)
    filename = f"informe_major_a_casa_{date.today().isoformat()}.pdf"
    return StreamingResponse(
        BytesIO(pdf_bytes), media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/casos/informe/pdf/renovacion", summary="Informe PDF de renovaciones del mes actual")
def generar_informe_renovacion_pdf(zona: Optional[int] = None, lang: str = "es", db: Session = Depends(get_db)):
    mes_actual = date.today().strftime("%Y-%m")
    lista_meses = _MESES_VAL if lang == "val" else _MESES_ES
    mes_nombre = lista_meses[date.today().month - 1].capitalize()

    q = db.query(CasoMayorACasa).filter(CasoMayorACasa.mes_renovacion == mes_actual)
    extra = f" — {mes_nombre} {date.today().year}"
    if zona:
        q = q.filter(CasoMayorACasa.zona == zona)
    casos = q.order_by(CasoMayorACasa.apellidos).all()
    pdf_bytes = _build_pdf(casos, titulo_key="renovacion", lang=lang, extra_titulo=extra)
    filename = f"renovacion_major_a_casa_{mes_actual}.pdf"
    return StreamingResponse(
        BytesIO(pdf_bytes), media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ═══════════════════════════════════════════════════════════════
#  ENDPOINTS — COMISIONES
# ═══════════════════════════════════════════════════════════════

@router.get("/comisiones/", response_model=List[ComisionResponse], summary="Listar comisiones")
def list_comisiones(
    zona:   Optional[int] = None,
    estado: Optional[str] = None,
    mes:    Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(ComisionMayorACasa)
    if zona:
        q = q.filter(ComisionMayorACasa.zona == zona)
    if estado:
        q = q.filter(ComisionMayorACasa.estado == estado)
    if mes:
        q = q.filter(ComisionMayorACasa.mes_comision == mes)
    return q.order_by(ComisionMayorACasa.apellidos).all()
@router.post("/comisiones/", response_model=ComisionResponse, status_code=201, summary="Crear comisión")
def create_comision(data: ComisionCreate, db: Session = Depends(get_db)):
    # Verificar duplicado
    if data.dni:
        exists = db.query(CasoMayorACasa).filter(CasoMayorACasa.dni == data.dni).first()
        if exists: raise HTTPException(status_code=400, detail="Ya existe un usuario con este DNI")
    if data.sip:
        exists = db.query(CasoMayorACasa).filter(CasoMayorACasa.sip == data.sip).first()
        if exists: raise HTTPException(status_code=400, detail="Ya existe un usuario con este SIP")

    if not data.mes_comision:
        data.mes_comision = date.today().strftime("%Y-%m")
    
    comision = ComisionMayorACasa(**data.model_dump())
    db.add(comision)
    db.commit()
    db.refresh(comision)
    return comision


@router.patch("/comisiones/{comision_id}", response_model=ComisionResponse, summary="Actualizar comisión")
def update_comision(comision_id: int, data: ComisionUpdate, db: Session = Depends(get_db)):
    comision = db.query(ComisionMayorACasa).filter(ComisionMayorACasa.id == comision_id).first()
    if not comision:
        raise HTTPException(status_code=404, detail=f"Comisión {comision_id} no encontrada")
    
    prev_estado = comision.estado
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(comision, field, value)
    
    # Si pasa a aprobado, crear usuario (Caso)
    if comision.estado == 'aprobado' and prev_estado != 'aprobado':
        # Verificar duplicado
        if comision.dni:
            exists = db.query(CasoMayorACasa).filter(CasoMayorACasa.dni == comision.dni).first()
            if exists: raise HTTPException(status_code=400, detail="Ya existe un usuario con este DNI")
        if comision.sip:
            exists = db.query(CasoMayorACasa).filter(CasoMayorACasa.sip == comision.sip).first()
            if exists: raise HTTPException(status_code=400, detail="Ya existe un usuario con este SIP")

        caso = CasoMayorACasa(
            apellidos=comision.apellidos,
            nombre=comision.nombre,
            dni=comision.dni,
            sip=comision.sip,
            zona=comision.zona,
            rango_edad=comision.rango_edad,
            sexo=comision.sexo,
            mes_renovacion=comision.mes_renovacion,
            telefono=comision.telefono,
            direccion=comision.direccion,
            fecha_alta=date.today(),
            observaciones=comision.observaciones,
            activo=True,
        )
        db.add(caso)
        db.flush()
        comision.caso_id = caso.id

    db.commit()
    db.refresh(comision)
    return comision


@router.delete("/comisiones/{comision_id}", status_code=204, summary="Eliminar comisión")
def delete_comision(comision_id: int, db: Session = Depends(get_db)):
    comision = db.query(ComisionMayorACasa).filter(ComisionMayorACasa.id == comision_id).first()
    if not comision:
        raise HTTPException(status_code=404, detail=f"Comisión {comision_id} no encontrada")
    db.delete(comision)
    db.commit()


@router.post("/comisiones/{comision_id}/aprobar", response_model=CasoResponse, summary="Aprobar comisión → crear caso")
def aprobar_comision(comision_id: int, db: Session = Depends(get_db)):
    comision = db.query(ComisionMayorACasa).filter(ComisionMayorACasa.id == comision_id).first()
    if not comision:
        raise HTTPException(status_code=404, detail=f"Comisión {comision_id} no encontrada")
    if comision.estado == 'aprobado' and comision.caso_id:
        raise HTTPException(status_code=400, detail="Esta comisión ya fue aprobada")

    # Verificar duplicado en Usuarios (Casos) antes de crear uno nuevo
    if comision.dni:
        exists = db.query(CasoMayorACasa).filter(CasoMayorACasa.dni == comision.dni).first()
        if exists: raise HTTPException(status_code=400, detail="Ya existe un usuario con este DNI")
    if comision.sip:
        exists = db.query(CasoMayorACasa).filter(CasoMayorACasa.sip == comision.sip).first()
        if exists: raise HTTPException(status_code=400, detail="Ya existe un usuario con este SIP")

    caso = CasoMayorACasa(
        apellidos=comision.apellidos,
        nombre=comision.nombre,
        dni=comision.dni,
        sip=comision.sip,
        zona=comision.zona,
        rango_edad=comision.rango_edad,
        sexo=comision.sexo,
        mes_renovacion=comision.mes_renovacion,
        telefono=comision.telefono,
        direccion=comision.direccion,
        fecha_alta=date.today(), # Fecha de alta automática hoy
        observaciones=comision.observaciones,
        activo=True,
    )
    db.add(caso)
    db.flush()

    comision.estado  = 'aprobado'
    comision.caso_id = caso.id
    db.commit()
    db.refresh(caso)
    return caso


# ═══════════════════════════════════════════════════════════════
#  ENDPOINTS — FACTURAS
# ═══════════════════════════════════════════════════════════════

@router.get("/facturas/", response_model=List[FacturaResponse], summary="Listar facturas")
def list_facturas(anio: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(FacturaMayorACasa)
    if anio:
        q = q.filter(FacturaMayorACasa.anio == anio)
    return q.order_by(FacturaMayorACasa.anio.desc(), FacturaMayorACasa.mes.asc()).all()


@router.put("/facturas/", response_model=FacturaResponse, summary="Crear o actualizar factura (upsert por año+mes)")
def upsert_factura(data: FacturaUpsert, db: Session = Depends(get_db)):
    existing = db.query(FacturaMayorACasa).filter(
        FacturaMayorACasa.anio == data.anio,
        FacturaMayorACasa.mes  == data.mes,
    ).first()
    if existing:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return existing
    factura = FacturaMayorACasa(**data.model_dump())
    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura


@router.post("/facturas/{factura_id}/pdf", summary="Subir PDF adjunto de factura")
async def upload_factura_pdf(
    factura_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    factura = db.query(FacturaMayorACasa).filter(FacturaMayorACasa.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"factura_{factura_id}.pdf"
    filepath = UPLOAD_DIR / filename
    content = await file.read()
    filepath.write_bytes(content)

    factura.pdf_filename = filename
    db.commit()
    db.refresh(factura)
    return {"pdf_url": f"/static/uploads/facturas/{filename}", "factura": FacturaResponse.model_validate(factura)}


@router.get("/facturas/{factura_id}/pdf", summary="Descargar PDF adjunto de factura")
def download_factura_pdf(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(FacturaMayorACasa).filter(FacturaMayorACasa.id == factura_id).first()
    if not factura or not factura.pdf_filename:
        raise HTTPException(status_code=404, detail="PDF no encontrado")
    filepath = UPLOAD_DIR / factura.pdf_filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado en servidor")
    return FileResponse(str(filepath), media_type="application/pdf",
                        filename=f"factura_{factura.anio}_{factura.mes:02d}.pdf")


@router.delete("/facturas/{factura_id}/pdf", status_code=204, summary="Eliminar PDF adjunto de factura")
def delete_factura_pdf(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(FacturaMayorACasa).filter(FacturaMayorACasa.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    if factura.pdf_filename:
        filepath = UPLOAD_DIR / factura.pdf_filename
        if filepath.exists():
            filepath.unlink()
        factura.pdf_filename = None
        db.commit()
    return
