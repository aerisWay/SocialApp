# ============================================================
# routers/mayor_a_casa.py — Endpoints del servicio Major a Casa
# ============================================================

from io import BytesIO
from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.caso_mayor_a_casa import CasoMayorACasa
from app.schemas.caso_mayor_a_casa import CasoCreate, CasoUpdate, CasoResponse
from app.utils.auth import get_current_dept

router = APIRouter(dependencies=[Depends(get_current_dept)])

STATIC_IMG = Path(__file__).parent.parent / "static" / "img"


# ── Localización PDF ───────────────────────────────────────────
PDF_I18N = {
    "es": {
        "activos": "Informe de Casos Activos",
        "renovacion": "Renovaciones",
        "generated": "Generado el",
        "total": "Total",
        "casos": "casos",
        "hombres": "Hombres",
        "mujeres": "Mujeres",
        "no_def": "No especificado",
        "headers": ["Apellidos", "Nombre", "DNI", "SIP", "Zona", "Sexo", "Teléfono", "Mes Renov.", "F. Alta", "Dirección"],
        "footer": "Concejalía de Bienestar Social — Ayto. Benidorm"
    },
    "val": {
        "activos": "Informe de Casos Actius",
        "renovacion": "Renovacions",
        "generated": "Generat el",
        "total": "Total",
        "casos": "casos",
        "hombres": "Homes",
        "mujeres": "Dones",
        "no_def": "No especificat",
        "headers": ["Cognoms", "Nom", "DNI", "SIP", "Zona", "Sexe", "Telèfon", "Mes Renov.", "F. Alta", "Adreça"],
        "footer": "Regidoria de Benestar Social — Ajunt. Benidorm"
    }
}


_MESES_ES = ["enero","febrero","marzo","abril","mayo","junio",
             "julio","agosto","septiembre","octubre","noviembre","diciembre"]
_MESES_VAL = ["gener","febrer","març","abril","maig","juny",
              "juliol","agost","setembre","octubre","novembre","desembre"]


# ── Helper: generar PDF ────────────────────────────────────────
def _build_pdf(casos: list, titulo_key: str = "activos", lang: str = "es", extra_titulo: str = "") -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle,
        Paragraph, Spacer, HRFlowable, Image,
    )

    t = PDF_I18N.get(lang, PDF_I18N["es"])
    titulo_base = t.get(titulo_key, titulo_key)
    titulo_full = f"Major a Casa — {titulo_base}{extra_titulo}"

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
        Paragraph(titulo_full, title_st),
        Paragraph(
            f"{t['generated']} {date.today().strftime('%d/%m/%Y')} · "
            f"{t['total']}: {len(casos)} {t['casos'] if 'casos' in t else 'casos'}",
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

    # Cabeceras locales
    headers = t["headers"]
    col_widths = [3.5*cm, 2.5*cm, 2.5*cm, 2*cm, 1.3*cm, 1.6*cm, 2.5*cm, 2*cm, 2*cm, None]

    def fmt_date(d): return d.strftime("%d/%m/%Y") if d else "—"
    def fmt_mes(m):  return m if m else "—"
    def fmt_zona(z): return f"Zona {z}" if z else "—"
    def fmt_sexo(s):
        return {"hombre": "Hombre", "mujer": "Mujer", "no_define": "No define"}.get(s or "", "—")

    data = [headers] + [
        [
            Paragraph(c.apellidos, cell_st),
            Paragraph(c.nombre, cell_st),
            c.dni or "—",
            c.sip or "—",
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
        ("BACKGROUND",   (0, 0), (-1, 0), azul),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING",(0, 0), (-1, 0), 8),
        ("TOPPADDING",   (0, 0), (-1, 0), 8),
        ("FONTSIZE",   (0, 1), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, claro]),
        ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#d0d7de")),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING",    (0, 1), (-1, -1), 5),
        ("ALIGN",      (4, 0), (4, -1), "CENTER"),
    ]))

    story.append(tabla)

    # Footer with text left + images right
    main_logo = STATIC_IMG / "MainLogo.png"
    second_logo = STATIC_IMG / "SecondLogo.png"

    def footer(canvas, _doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(gris)
        canvas.drawString(
            1.5 * cm, 1.2 * cm,
            t["footer"],
        )
        # Draw logos on the right if they exist
        page_w = landscape(A4)[0]
        x_right = page_w - 1.5 * cm
        logo_h = 0.8 * cm
        if second_logo.exists():
            try:
                canvas.drawImage(
                    str(second_logo), x_right - 4.2 * cm, 0.8 * cm,
                    width=4 * cm, height=1.6 * cm, preserveAspectRatio=True, mask='auto',
                )
                x_right -= 4.5 * cm
            except Exception:
                pass
        if main_logo.exists():
            try:
                canvas.drawImage(
                    str(main_logo), x_right - 1.2 * cm, 0.8 * cm,
                    width=1 * cm, height=0.4 * cm, preserveAspectRatio=True, mask='auto',
                )
            except Exception:
                pass
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
    # Check uniqueness on DNI and SIP separately
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
def generar_informe_pdf(zona: int | None = None, lang: str = "es", db: Session = Depends(get_db)):
    q = db.query(CasoMayorACasa).filter(CasoMayorACasa.activo == True)
    extra = f" — Zona {zona}" if zona else ""
    if zona:
        q = q.filter(CasoMayorACasa.zona == zona)
    
    casos = q.order_by(CasoMayorACasa.apellidos).all()
    pdf_bytes = _build_pdf(casos, titulo_key="activos", lang=lang, extra_titulo=extra)
    filename = f"informe_major_a_casa_{date.today().isoformat()}.pdf"
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


_MESES_ES = ["enero","febrero","marzo","abril","mayo","junio",
             "julio","agosto","septiembre","octubre","noviembre","diciembre"]


@router.get("/casos/informe/pdf/renovacion", summary="Informe PDF de renovaciones del mes actual")
def generar_informe_renovacion_pdf(zona: int | None = None, lang: str = "es", db: Session = Depends(get_db)):
    mes_actual = date.today().strftime("%Y-%m")
    
    lista_meses = _MESES_VAL if lang == "val" else _MESES_ES
    mes_nombre = lista_meses[date.today().month - 1].capitalize()
    
    q = db.query(CasoMayorACasa).filter(CasoMayorACasa.mes_renovacion == mes_actual)
    extra = f" — {mes_nombre} {date.today().year}"
    if zona:
        q = q.filter(CasoMayorACasa.zona == zona)
        extra += f" — Zona {zona}"
        
    casos = q.order_by(CasoMayorACasa.apellidos).all()
    pdf_bytes = _build_pdf(casos, titulo_key="renovacion", lang=lang, extra_titulo=extra)
    filename = f"renovacion_{mes_actual}.pdf"
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
