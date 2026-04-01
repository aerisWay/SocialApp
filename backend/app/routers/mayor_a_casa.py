# ============================================================
# routers/mayor_a_casa.py — Endpoints del servicio Mayor a Casa
# ============================================================

from io import BytesIO
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.caso_mayor_a_casa import CasoMayorACasa
from app.schemas.caso_mayor_a_casa import CasoCreate, CasoUpdate, CasoResponse
from app.utils.auth import get_current_dept

# dependencies=[Depends(get_current_dept)] protege TODOS los endpoints del router con una sola línea
router = APIRouter(dependencies=[Depends(get_current_dept)])


# ── Helper: generar PDF ────────────────────────────────────────
def _build_pdf(casos: list, titulo: str = "Informe de Casos Activos") -> bytes:
    """Genera un PDF con la lista de casos usando ReportLab."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle,
        Paragraph, Spacer, HRFlowable,
    )

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=1.5 * cm, leftMargin=1.5 * cm,
        topMargin=2.2 * cm,   bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    azul   = colors.HexColor("#1f6feb")
    gris   = colors.HexColor("#6e7681")
    claro  = colors.HexColor("#f6f8fa")

    title_st = ParagraphStyle(
        "title", parent=styles["Heading1"],
        fontSize=18, textColor=azul,
        spaceAfter=4, alignment=TA_CENTER,
    )
    sub_st = ParagraphStyle(
        "sub", parent=styles["Normal"],
        fontSize=10, textColor=gris,
        spaceAfter=16, alignment=TA_CENTER,
    )
    cell_st = ParagraphStyle("cell", parent=styles["Normal"], fontSize=8)

    hombres = sum(1 for c in casos if c.sexo == "hombre")
    mujeres = sum(1 for c in casos if c.sexo == "mujer")
    no_def  = len(casos) - hombres - mujeres

    stats_st = ParagraphStyle(
        "stats", parent=styles["Normal"],
        fontSize=9, textColor=azul,
        spaceAfter=10, alignment=TA_CENTER,
    )

    story = [
        Paragraph(f"Mayor a Casa — {titulo}", title_st),
        Paragraph(
            f"Generado el {date.today().strftime('%d/%m/%Y')} · "
            f"Total: {len(casos)} caso{'s' if len(casos) != 1 else ''}",
            sub_st,
        ),
        Paragraph(
            f"Hombres: <b>{hombres}</b>   ·   Mujeres: <b>{mujeres}</b>"
            + (f"   ·   No especificado: <b>{no_def}</b>" if no_def > 0 else ""),
            stats_st,
        ),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e1e4e8")),
        Spacer(1, 0.4 * cm),
    ]

    # Cabeceras
    headers = [
        "Apellidos", "Nombre", "DNI / SIP", "Zona", "Sexo",
        "Teléfono", "Mes Renov.", "F. Alta", "Dirección",
    ]
    col_widths = [4*cm, 3*cm, 2.8*cm, 1.5*cm, 1.8*cm, 2.8*cm, 2.2*cm, 2.2*cm, None]

    def fmt_date(d): return d.strftime("%d/%m/%Y") if d else "—"
    def fmt_mes(m):  return m if m else "—"
    def fmt_zona(z): return f"Zona {z}" if z else "—"
    def fmt_sexo(s):
        return {"hombre": "Hombre", "mujer": "Mujer", "no_define": "No define"}.get(s or "", "—")

    # Filas de datos
    data = [headers] + [
        [
            Paragraph(c.apellidos, cell_st),
            Paragraph(c.nombre, cell_st),
            c.dni_sip,
            fmt_zona(c.zona),
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
        # Cabecera
        ("BACKGROUND",   (0, 0), (-1, 0), azul),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING",(0, 0), (-1, 0), 8),
        ("TOPPADDING",   (0, 0), (-1, 0), 8),
        # Filas
        ("FONTSIZE",   (0, 1), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, claro]),
        ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#d0d7de")),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING",    (0, 1), (-1, -1), 5),
        ("ALIGN",      (3, 0), (3, -1), "CENTER"),  # Zona centrada
    ]))

    story.append(tabla)

    # Pie de página con número de página
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(gris)
        canvas.drawString(1.5 * cm, 1.2 * cm, "SocialApp — Informe Mayor a Casa")
        canvas.drawRightString(
            landscape(A4)[0] - 1.5 * cm, 1.2 * cm,
            f"Página {canvas.getPageNumber()}",
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return buffer.getvalue()


# ── ENDPOINTS ──────────────────────────────────────────────────

@router.get("/casos/", response_model=List[CasoResponse], summary="Listar todos los casos")
def list_casos(
    solo_activos: bool = False,
    zona: int | None = None,
    db: Session = Depends(get_db),
):
    """Devuelve todos los casos. Filtros opcionales: solo_activos, zona."""
    q = db.query(CasoMayorACasa)
    if solo_activos:
        q = q.filter(CasoMayorACasa.activo == True)
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
    if db.query(CasoMayorACasa).filter(CasoMayorACasa.dni_sip == data.dni_sip).first():
        raise HTTPException(status_code=400, detail="Ya existe un caso con ese DNI/SIP")
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
def generar_informe_pdf(db: Session = Depends(get_db)):
    """Genera y descarga un PDF con todos los casos activos, ordenados por apellidos."""
    casos = (
        db.query(CasoMayorACasa)
        .filter(CasoMayorACasa.activo == True)
        .order_by(CasoMayorACasa.apellidos)
        .all()
    )
    pdf_bytes = _build_pdf(casos, titulo="Informe de Casos Activos")
    filename = f"informe_mayor_a_casa_{date.today().isoformat()}.pdf"
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


_MESES_ES = ["enero","febrero","marzo","abril","mayo","junio",
             "julio","agosto","septiembre","octubre","noviembre","diciembre"]


@router.get("/casos/informe/pdf/renovacion", summary="Informe PDF de renovaciones del mes actual")
def generar_informe_renovacion_pdf(db: Session = Depends(get_db)):
    """Genera y descarga un PDF con los casos cuya renovación coincide con el mes actual."""
    mes_actual = date.today().strftime("%Y-%m")
    mes_nombre = _MESES_ES[date.today().month - 1].capitalize()
    casos = (
        db.query(CasoMayorACasa)
        .filter(CasoMayorACasa.mes_renovacion == mes_actual)
        .order_by(CasoMayorACasa.apellidos)
        .all()
    )
    pdf_bytes = _build_pdf(casos, titulo=f"Renovaciones — {mes_nombre} {date.today().year}")
    filename = f"renovacion_{mes_actual}.pdf"
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
