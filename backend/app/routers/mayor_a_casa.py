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
from app.models.seguimiento_mayor_a_casa import SeguimientoMayorACasa
from app.models.documentacion_mayor_a_casa import DocumentacionMayorACasa
from app.schemas.caso_mayor_a_casa import CasoCreate, CasoUpdate, CasoResponse
from app.schemas.comision_mayor_a_casa import ComisionCreate, ComisionUpdate, ComisionResponse
from app.schemas.factura_mayor_a_casa import FacturaUpsert, FacturaResponse
from app.schemas.seguimiento_mayor_a_casa import SeguimientoUpsert, SeguimientoResponse
from app.schemas.documentacion_mayor_a_casa import DocumentacionCreate, DocumentacionUpdate, DocumentacionResponse
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

    footer = _make_footer(lang)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return buffer.getvalue()


# ── Helper: pie de página compartido ─────────────────────────
def _make_footer(lang: str = "es"):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import cm
    t = PDF_I18N.get(lang, PDF_I18N["es"])
    gris = colors.HexColor("#6e7681")
    main_logo   = STATIC_IMG / "MainLogo.png"
    second_logo = STATIC_IMG / "SecondLogo.png"

    def footer(canvas, _doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(gris)
        canvas.drawString(1.5 * cm, 1.0 * cm, t["footer"])
        page_w, _ = canvas.getPageSize()
        x_right = page_w - 1.5 * cm
        if second_logo.exists():
            try:
                canvas.drawImage(str(second_logo), x_right - 8.5 * cm, 0.3 * cm,
                                 width=8 * cm, height=3.2 * cm,
                                 preserveAspectRatio=True, mask='auto-opaque')
                x_right -= 8.8 * cm
            except Exception:
                pass
        if main_logo.exists():
            try:
                canvas.drawImage(str(main_logo), x_right - 0.6 * cm, 0.8 * cm,
                                 width=0.5 * cm, height=0.2 * cm,
                                 preserveAspectRatio=True, mask='auto')
            except Exception:
                pass
        canvas.restoreState()
    return footer


# ── Helper: PDF Facturas ──────────────────────────────────────
def _build_pdf_facturas(facturas: list, anio: int, lang: str = "es") -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable

    t  = PDF_I18N.get(lang, PDF_I18N["es"])
    meses = _MESES_VAL if lang == "val" else _MESES_ES
    azul  = colors.HexColor("#1f6feb")
    gris  = colors.HexColor("#6e7681")
    claro = colors.HexColor("#f6f8fa")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2.2*cm, bottomMargin=2.5*cm)
    styles = getSampleStyleSheet()
    title_st = ParagraphStyle("t", parent=styles["Heading1"],
                              fontSize=18, textColor=azul, spaceAfter=4, alignment=TA_CENTER)
    sub_st   = ParagraphStyle("s", parent=styles["Normal"],
                              fontSize=10, textColor=gris, spaceAfter=16, alignment=TA_CENTER)
    num_st   = ParagraphStyle("n", parent=styles["Normal"],
                              fontSize=9, alignment=TA_RIGHT)
    cell_st  = ParagraphStyle("c", parent=styles["Normal"], fontSize=9, alignment=TA_CENTER)

    by_mes = {f.mes: f for f in facturas}
    total_casos   = sum((f.num_casos or 0) for f in facturas)
    total_cuantia = float(sum((f.cuantia or 0) for f in facturas))

    story = [
        Paragraph(f"Major a Casa — Facturacion {anio}", title_st),
        Paragraph(f"{t['generated']} {date.today().strftime('%d/%m/%Y')}", sub_st),
        Spacer(1, 0.4*cm),
    ]

    headers = [
        Paragraph("<b>Mes</b>", cell_st),
        Paragraph("<b>N. Casos</b>", cell_st),
        Paragraph("<b>% Casos</b>", cell_st),
        Paragraph("<b>Cuantia (EUR)</b>", cell_st),
        Paragraph("<b>% Cuantia</b>", cell_st)
    ]
    data = [headers]
    for i, mes_nom in enumerate(meses):
        mes = i + 1
        f = by_mes.get(mes)
        casos   = f.num_casos if f and f.num_casos is not None else 0
        cuantia = float(f.cuantia or 0) if f else 0
        pct_c  = f"{(casos / total_casos * 100):.1f}%" if total_casos else "—"
        pct_q  = f"{(cuantia / total_cuantia * 100):.1f}%" if total_cuantia else "—"
        data.append([
            mes_nom.capitalize(),
            Paragraph(str(casos) if casos else "—", num_st),
            Paragraph(pct_c, num_st),
            Paragraph(f"{cuantia:,.2f}" if cuantia else "—", num_st),
            Paragraph(pct_q, num_st),
        ])

    data.append([
        Paragraph("<b>TOTAL</b>", cell_st),
        Paragraph(f"<b>{total_casos}</b>", num_st),
        Paragraph("<b>100%</b>" if total_casos else "—", num_st),
        Paragraph(f"<b>{total_cuantia:,.2f}</b>", num_st),
        Paragraph("<b>100%</b>" if total_cuantia else "—", num_st),
    ])

    col_w = [3.5*cm, 2.5*cm, 2.5*cm, 4.5*cm, 2.5*cm]
    n_rows = len(data)
    tabla = Table(data, colWidths=col_w, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), azul),
        ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS",(0, 1), (-1, n_rows-2), [colors.white, claro]),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#d0d7de")),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(tabla)

    footer = _make_footer(lang)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return buffer.getvalue()


# ── Helper: PDF Comisiones ────────────────────────────────────
def _build_pdf_comisiones(comisiones: list, lang: str = "es",
                           zona: Optional[int] = None, mes: Optional[str] = None) -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable

    t     = PDF_I18N.get(lang, PDF_I18N["es"])
    azul  = colors.HexColor("#1f6feb")
    gris  = colors.HexColor("#6e7681")
    claro = colors.HexColor("#f6f8fa")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                            rightMargin=1.5*cm, leftMargin=1.5*cm,
                            topMargin=2.2*cm,   bottomMargin=2.5*cm)
    styles = getSampleStyleSheet()
    title_st = ParagraphStyle("t", parent=styles["Heading1"],
                              fontSize=18, textColor=azul, spaceAfter=4, alignment=TA_CENTER)
    sub_st   = ParagraphStyle("s", parent=styles["Normal"],
                              fontSize=10, textColor=gris, spaceAfter=8, alignment=TA_CENTER)
    cell_st  = ParagraphStyle("c", parent=styles["Normal"], fontSize=8)

    filtros = []
    if zona: filtros.append(f"Zona {zona}")
    if mes:  filtros.append(f"Mes: {mes}")
    filtro_txt = " · ".join(filtros) if filtros else ("Todas las zonas" if lang == "es" else "Totes les zones")

    hombres = sum(1 for c in comisiones if c.sexo == "hombre")
    mujeres = sum(1 for c in comisiones if c.sexo == "mujer")

    story = [
        Paragraph("Major a Casa — Comisiones en Trámite", title_st),
        Paragraph(f"{t['generated']} {date.today().strftime('%d/%m/%Y')} · Filtro: {filtro_txt}", sub_st),
        Paragraph(
            f"Total: <b>{len(comisiones)}</b>   ·   "
            f"{'Hombres' if lang=='es' else 'Homes'}: <b>{hombres}</b>   ·   "
            f"{'Mujeres' if lang=='es' else 'Dones'}: <b>{mujeres}</b>",
            ParagraphStyle("st", parent=styles["Normal"], fontSize=9, textColor=azul,
                           spaceAfter=10, alignment=TA_CENTER)
        ),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e1e4e8")),
        Spacer(1, 0.4*cm),
    ]

    headers = (["Apellidos", "Nombre", "DNI", "SIP", "Zona", "Edad", "Sexo", "Mes Com.", "Estado"]
               if lang == "es" else
               ["Cognoms", "Nom", "DNI", "SIP", "Zona", "Edat", "Sexe", "Mes Com.", "Estat"])

    estado_labels = {"en_tramite": "En trámite", "aprobado": "Aprobado", "denegado": "Denegado"}
    if lang == "val":
        estado_labels = {"en_tramite": "En tràmit", "aprobado": "Aprovat", "denegado": "Denegat"}

    def fmt_edad(e): return t.get(e, "—") if e else "—"
    def fmt_sexo(s):
        m = {"hombre": "Hombre", "mujer": "Mujer", "no_define": "N/D"} if lang == "es" \
            else {"hombre": "Home",  "mujer": "Dona",  "no_define": "N/D"}
        return m.get(s or "", "—")

    data = [headers] + [
        [
            Paragraph(c.apellidos or "—", cell_st),
            Paragraph(c.nombre    or "—", cell_st),
            c.dni or "—",
            c.sip or "—",
            f"Zona {c.zona}" if c.zona else "—",
            fmt_edad(c.rango_edad),
            fmt_sexo(c.sexo),
            c.mes_comision or "—",
            estado_labels.get(c.estado, c.estado or "—"),
        ]
        for c in comisiones
    ]

    col_w = [3*cm, 2*cm, 2.2*cm, 2*cm, 1.4*cm, 1.4*cm, 1.6*cm, 2.2*cm, 2*cm] # Reduced for landscape
    tabla = Table(data, colWidths=col_w, repeatRows=1)
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
    ]))
    story.append(tabla)

    footer = _make_footer(lang)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return buffer.getvalue()


# ── Helper: PDF Seguimiento ───────────────────────────────────
def _build_pdf_seguimiento(rows: list, tipo: str, anio: int, lang: str = "es") -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable

    t     = PDF_I18N.get(lang, PDF_I18N["es"])
    meses = _MESES_VAL if lang == "val" else _MESES_ES
    azul  = colors.HexColor("#1f6feb")
    gris  = colors.HexColor("#6e7681")
    claro = colors.HexColor("#f6f8fa")
    verde = colors.HexColor("#0d6e3f")

    tipo_labels = {
        "entrevista": ("Entrevistas" if lang == "es" else "Entrevistes"),
        "visita":     ("Visitas"     if lang == "es" else "Visites"),
        "informe":    ("Informes"    if lang == "es" else "Informes"),
    }
    tipo_label = tipo_labels.get(tipo, tipo.capitalize())

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2.2*cm, bottomMargin=2.5*cm)
    styles = getSampleStyleSheet()
    title_st = ParagraphStyle("t", parent=styles["Heading1"],
                              fontSize=18, textColor=azul, spaceAfter=4, alignment=TA_CENTER)
    sub_st   = ParagraphStyle("s", parent=styles["Normal"],
                              fontSize=10, textColor=gris, spaceAfter=16, alignment=TA_CENTER)
    num_st   = ParagraphStyle("n", parent=styles["Normal"], fontSize=9, alignment=TA_RIGHT)

    by_mes    = {r.mes: r for r in rows}
    total_c   = sum(r.cantidad or 0 for r in rows)
    total_h   = sum(r.hombres  or 0 for r in rows)
    total_m   = sum(r.mujeres  or 0 for r in rows)

    story = [
        Paragraph(f"Major a Casa — Seguimiento: {tipo_label} {anio}", title_st),
        Paragraph(f"{t['generated']} {date.today().strftime('%d/%m/%Y')}", sub_st),
        Paragraph(
            f"Total: <b>{total_c}</b>   ·   "
            f"{'Hombres' if lang=='es' else 'Homes'}: <b>{total_h}</b>   ·   "
            f"{'Mujeres' if lang=='es' else 'Dones'}: <b>{total_m}</b>",
            ParagraphStyle("st", parent=styles["Normal"], fontSize=9, textColor=azul,
                           spaceAfter=10, alignment=TA_CENTER)
        ),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e1e4e8")),
        Spacer(1, 0.4*cm),
    ]

    col_h = ["Mes", "Cantidad", "Hombres", "% Hombres", "Mujeres", "% Mujeres"] if lang == "es" \
            else ["Mes", "Quantitat", "Homes", "% Homes", "Dones", "% Dones"]

    data = [col_h]
    for i, mes_nom in enumerate(meses):
        mes = i + 1
        r   = by_mes.get(mes)
        c   = r.cantidad or 0 if r else 0
        h   = r.hombres  or 0 if r else 0
        m   = r.mujeres  or 0 if r else 0
        pct_h = f"{(h/c*100):.1f}%" if c else "—"
        pct_m = f"{(m/c*100):.1f}%" if c else "—"
        data.append([
            mes_nom.capitalize(),
            Paragraph(str(c) if c else "—", num_st),
            Paragraph(str(h) if h else "—", num_st),
            Paragraph(pct_h,                num_st),
            Paragraph(str(m) if m else "—", num_st),
            Paragraph(pct_m,                num_st),
        ])
    # Totals
    pct_ht = f"{(total_h/total_c*100):.1f}%" if total_c else "—"
    pct_mt = f"{(total_m/total_c*100):.1f}%" if total_c else "—"
    data.append([
        "TOTAL",
        Paragraph(f"<b>{total_c}</b>", num_st),
        Paragraph(f"<b>{total_h}</b>", num_st),
        Paragraph(f"<b>{pct_ht}</b>",  num_st),
        Paragraph(f"<b>{total_m}</b>", num_st),
        Paragraph(f"<b>{pct_mt}</b>",  num_st),
    ])

    col_w = [3.5*cm, 2.5*cm, 2.3*cm, 2.3*cm, 2.3*cm, 2.3*cm] # Total 15.2cm
    n     = len(data)
    tabla = Table(data, colWidths=col_w, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), azul),
        ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING",    (0, 0), (-1, 0), 8),
        ("FONTSIZE",      (0, 1), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, n-2), [colors.white, claro]),
        ("BACKGROUND",    (0, n-1), (-1, n-1), colors.HexColor("#e8f5e9")),
        ("TEXTCOLOR",     (0, n-1), (-1, n-1), verde),
        ("FONTNAME",      (0, n-1), (-1, n-1), "Helvetica-Bold"),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#d0d7de")),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",         (0, 0), (0, -1), "LEFT"),
        ("PADDING",       (0, 1), (-1, -1), 5),
    ]))
    story.append(tabla)

    footer = _make_footer(lang)
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


# ─── PDF Facturas ─────────────────────────────────────────────
@router.get("/facturas/informe/pdf", summary="Informe PDF de facturación anual")
def informe_facturas_pdf(
    anio: Optional[str] = None,
    lang: str = "es",
    db: Session = Depends(get_db),
):
    try:
        real_anio = date.today().year
        if anio and anio.isdigit():
            real_anio = int(anio)
        
        facturas = db.query(FacturaMayorACasa).filter(FacturaMayorACasa.anio == real_anio).all()
        pdf_bytes = _build_pdf_facturas(facturas, anio=real_anio, lang=lang)
        filename  = f"facturas_major_a_casa_{real_anio}.pdf"
        return StreamingResponse(
            BytesIO(pdf_bytes), media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        import traceback
        err_msg = traceback.format_exc()
        with open("/tmp/pdf_error.log", "w", encoding="utf-8") as f:
            f.write(err_msg)
        raise HTTPException(status_code=500, detail=str(e))


# ─── PDF Comisiones ───────────────────────────────────────────
@router.get("/comisiones/informe/pdf", summary="Informe PDF de comisiones en trámite")
def informe_comisiones_pdf(
    zona:   Optional[int] = None,
    mes:    Optional[str] = None,
    lang:   str = "es",
    db: Session = Depends(get_db),
):
    q = db.query(ComisionMayorACasa).filter(ComisionMayorACasa.estado == "en_tramite")
    if zona: q = q.filter(ComisionMayorACasa.zona == zona)
    if mes:  q = q.filter(ComisionMayorACasa.mes_comision == mes)
    comisiones = q.order_by(ComisionMayorACasa.apellidos).all()
    pdf_bytes  = _build_pdf_comisiones(comisiones, lang=lang, zona=zona, mes=mes)
    filename   = f"comisiones_tramite_{date.today().isoformat()}.pdf"
    return StreamingResponse(
        BytesIO(pdf_bytes), media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ─── PDF Seguimiento ──────────────────────────────────────────
@router.get("/seguimientos/informe/pdf", summary="Informe PDF de seguimiento")
def informe_seguimiento_pdf(
    tipo: str = "entrevista",
    anio: Optional[int] = None,
    lang: str = "es",
    db: Session = Depends(get_db),
):
    anio  = anio or date.today().year
    rows  = db.query(SeguimientoMayorACasa).filter(
        SeguimientoMayorACasa.tipo == tipo,
        SeguimientoMayorACasa.anio == anio,
    ).order_by(SeguimientoMayorACasa.mes).all()
    pdf_bytes = _build_pdf_seguimiento(rows, tipo=tipo, anio=anio, lang=lang)
    filename  = f"seguimiento_{tipo}_{anio}.pdf"
    return StreamingResponse(
        BytesIO(pdf_bytes), media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


UPLOAD_DIR_DOC = Path(__file__).parent.parent / "static" / "uploads" / "documentacion"

# ═══════════════════════════════════════════════════════════════
#  ENDPOINTS — SEGUIMIENTO (Entrevistas / Visitas / Informes)
# ═══════════════════════════════════════════════════════════════

@router.get("/seguimientos/", response_model=List[SeguimientoResponse], summary="Listar seguimientos")
def list_seguimientos(
    tipo: Optional[str] = None,
    anio: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(SeguimientoMayorACasa)
    if tipo:
        q = q.filter(SeguimientoMayorACasa.tipo == tipo)
    if anio:
        q = q.filter(SeguimientoMayorACasa.anio == anio)
    return q.order_by(SeguimientoMayorACasa.tipo, SeguimientoMayorACasa.anio, SeguimientoMayorACasa.mes).all()


@router.put("/seguimientos/", response_model=SeguimientoResponse, summary="Crear o actualizar seguimiento (upsert)")
def upsert_seguimiento(data: SeguimientoUpsert, db: Session = Depends(get_db)):
    existing = db.query(SeguimientoMayorACasa).filter(
        SeguimientoMayorACasa.tipo == data.tipo,
        SeguimientoMayorACasa.anio == data.anio,
        SeguimientoMayorACasa.mes  == data.mes,
    ).first()
    if existing:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return existing
    seg = SeguimientoMayorACasa(**data.model_dump())
    db.add(seg)
    db.commit()
    db.refresh(seg)
    return seg


# ═══════════════════════════════════════════════════════════════
#  ENDPOINTS — DOCUMENTACIÓN
# ═══════════════════════════════════════════════════════════════

@router.get("/documentacion/", response_model=List[DocumentacionResponse], summary="Listar documentos")
def list_documentacion(db: Session = Depends(get_db)):
    return db.query(DocumentacionMayorACasa).order_by(DocumentacionMayorACasa.titulo).all()


@router.post("/documentacion/", response_model=DocumentacionResponse, status_code=201, summary="Crear documento")
def create_documentacion(data: DocumentacionCreate, db: Session = Depends(get_db)):
    doc = DocumentacionMayorACasa(titulo=data.titulo)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.patch("/documentacion/{doc_id}", response_model=DocumentacionResponse, summary="Actualizar documento")
def update_documentacion(doc_id: int, data: DocumentacionUpdate, db: Session = Depends(get_db)):
    doc = db.query(DocumentacionMayorACasa).filter(DocumentacionMayorACasa.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(doc, field, value)
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/documentacion/{doc_id}", status_code=204, summary="Eliminar documento")
def delete_documentacion(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(DocumentacionMayorACasa).filter(DocumentacionMayorACasa.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    if doc.pdf_filename:
        filepath = UPLOAD_DIR_DOC / doc.pdf_filename
        if filepath.exists():
            filepath.unlink()
    db.delete(doc)
    db.commit()


@router.post("/documentacion/{doc_id}/pdf", summary="Subir PDF de documentación")
async def upload_documentacion_pdf(
    doc_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    doc = db.query(DocumentacionMayorACasa).filter(DocumentacionMayorACasa.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    UPLOAD_DIR_DOC.mkdir(parents=True, exist_ok=True)
    filename = f"doc_{doc_id}.pdf"
    (UPLOAD_DIR_DOC / filename).write_bytes(await file.read())
    doc.pdf_filename = filename
    db.commit()
    db.refresh(doc)
    return {"pdf_url": f"/static/uploads/documentacion/{filename}", "doc": DocumentacionResponse.model_validate(doc)}


@router.delete("/documentacion/{doc_id}/pdf", status_code=204, summary="Eliminar PDF de documentación")
def delete_documentacion_pdf(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(DocumentacionMayorACasa).filter(DocumentacionMayorACasa.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    if doc.pdf_filename:
        filepath = UPLOAD_DIR_DOC / doc.pdf_filename
        if filepath.exists():
            filepath.unlink()
        doc.pdf_filename = None
        db.commit()
    return
