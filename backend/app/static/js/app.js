/* ============================================================
   app.js — Lógica del frontend de APBApp
   ============================================================ */

'use strict';

// ── i18n — Traducciones ES / VAL ─────────────────────────────

const I18N = {
  es: {
    login_sub:     'Acceso para APB — Concejalía de Bienestar Social',
    login_footer:  'La sesión dura 8 horas · Token cifrado JWT',
    lbl_usuario:   'Usuario del departamento',
    lbl_password:  'Contraseña',
    btn_login:     'Iniciar sesión',
    btn_logout:    'Cerrar sesión',
    view_title:    'Menjar a Casa',
    itab_usuarios:  '👥 Usuarios',
    itab_facturas:  '🧾 Facturas',
    itab_comisiones:'📋 Comisiones',
    stat_total:    'Total casos',
    stat_activos:  'Activos',
    stat_bajas:    'Dados de baja',
    stat_zonas:    'Zonas con casos',
    stat_hombres:  'Hombres',
    stat_mujeres:  'Mujeres',
    comision_total: 'Total comisiones',
    stat_tramite:   'En trámite',
    stat_aprobadas: 'Aprobadas',
    stat_denegadas: 'Denegadas',
    chart_edad_title: 'Distribución por edad',
    lbl_zona:      'Zona:',
    zona_todas:    'Todas',
    lbl_ordenar:   'Ordenar:',
    sort_nombre:   'Nombre',
    sort_renov:    'Renovación',
    sort_alta:     'Alta',
    sort_estado:   'Estado',
    sip_search_placeholder: 'Buscar por SIP…',
    th_nombre:     'Apellidos, Nombre',
    th_zona:       'Zona',
    th_edad:       'Edad',
    th_sexo:       'Sexo',
    th_telefono:   'Teléfono',
    th_renov:      'Mes Renov.',
    th_alta:       'Fecha Alta',
    th_estado:     'Estado',
    th_estado_comision: 'Estado',
    th_acciones:   'Acciones',
    loading:       'Cargando casos…',
    btn_pdf:       '<span>📊</span> Generar Informe PDF',
    pdf_activos:   '📋 Todos los casos activos',
    pdf_renov:     '📅 Renovación del mes actual',
    btn_nuevo:     '<span>✦</span> Nuevo caso',
    btn_nuevo_comision: '<span>✦</span> Nueva comisión',
    btn_aprobar:   '✓ Aprobar y crear usuario',
    lbl_apellidos: 'Apellidos <span class="req">*</span>',
    lbl_nombre:    'Nombre <span class="req">*</span>',
    lbl_dni:       'DNI',
    lbl_sip:       'SIP <span class="field-hint-inline">(8 dígitos)</span>',
    hint_dni:      '8 dígitos + 1 letra',
    hint_sip_inline: '(8 dígitos)',
    lbl_zona_field:'Zona',
    lbl_rango_edad:'Rango de edad',
    opt_menor_60:  '< 60 años',
    opt_60_65:     '60-65 años',
    opt_mayor_65:  '> 65 años',
    lbl_sexo:      'Sexo',
    lbl_telefono:  'Teléfono',
    lbl_renov:     'Mes de renovación',
    lbl_alta:      'Fecha de alta',
    lbl_baja:      'Fecha de baja',
    lbl_direccion: 'Dirección',
    lbl_estado:    'Estado del caso',
    lbl_estado_comision: 'Estado de la comisión',
    lbl_obs:       'Observaciones / Notas',
    btn_eliminar:  '🗑️ Eliminar',
    btn_cancelar:  'Cancelar',
    btn_guardar:   'Guardar',
    modal_new:     'Nuevo Caso',
    modal_edit:    'Editar Caso',
    modal_new_com: 'Nueva Comisión',
    modal_edit_com:'Editar Comisión',
    modal_sub_new: 'Rellena los datos',
    sex_hombre:    'Hombre',
    sex_mujer:     'Mujer',
    sex_no_define: 'No define',
    badge_activo:  '● Activo',
    badge_baja:    '○ Baja',
    badge_tramite: '◎ En trámite',
    badge_aprobado:'✓ Aprobado',
    badge_denegado:'✗ Denegado',
    badge_tramite_opt:  'En trámite',
    badge_aprobado_opt: 'Aprobado',
    badge_denegado_opt: 'Denegado',
    empty_no_data: 'No hay registros.',
    empty_no_filter:'Sin resultados para el filtro aplicado.',
    toggle_activo: 'Activo',
    toggle_baja:   'Dado de baja',
    toast_saved:   'Guardado correctamente',
    toast_deleted: 'Eliminado',
    toast_load_err:'Error al cargar datos',
    toast_pdf_ok:  'PDF descargado',
    toast_pdf_err: 'Error al generar PDF',
    toast_approved:'Comisión aprobada — usuario creado',
    confirm_del:   '¿Eliminar registro de',
    confirm_aprobar: '¿Aprobar la comisión de',
    login_empty:   'Introduce usuario y contraseña',
    login_verify:  'Verificando...',
    pdf_generating:'<span>⏳</span> Generando...',
    val_required:  'Campos obligatorios faltantes',
    val_dni_or_sip:'Debes introducir al menos DNI o SIP',
    val_dni_bad:   'El DNI debe tener 8 dígitos y 1 letra (ej: 12345678X)',
    val_sip_bad:   'El SIP debe tener exactamente 8 dígitos',
    welcome:       'Bienvenido,',
    opt_no_asignar:'— Sin asignar —',
    opt_no_sexo:   '— No especificado —',
    facturas_title:'Facturas anuales',
    facturas_anio: 'Año:',
    th_mes:        'Mes',
    th_num_casos:  'Nº Casos',
    th_cuantia:    'Cuantía (€)',
    th_pdf_adjunto:'PDF Adjunto',
    btn_subir_pdf: 'Subir PDF',
    btn_ver_pdf:   'Ver PDF',
    btn_cambiar_pdf: 'Cambiar',
    btn_quitar_pdf: 'Eliminar PDF',
    confirm_quitar_pdf: '¿Seguro que quieres eliminar el PDF adjunto?',
    toast_pdf_deleted: 'PDF eliminado correctamente',
    lbl_mes:       'Mes:',
    chart_edad_title:  'Distribución por Edad',
    chart_sexo_title:  'Distribución por Género',
    chart_estado_title: 'Distribución por Estado',
    chart_estado_com_title: 'Estado de Tramitación',
    pdf_fact_anual:    '📋 Facturación del año seleccionado',
    pdf_com_tramite:   '📋 Comisiones en trámite',
    toast_pdf_facturas_err: 'Error al generar PDF de facturas',
    toast_pdf_com_err:      'Error al generar PDF de comisiones',
    toast_pdf_seg_err:      'Error al generar PDF de seguimiento',
    itab_seguimiento:  '📊 Seguimiento',
    itab_documentacion:'📁 Documentación',
    seg_title:         'Seguimiento anual',
    seg_entrevistas:   '🗣 Entrevistas',
    seg_visitas:       '🚪 Visitas',
    seg_informes:      '📄 Informes',
    seg_th_cantidad:   'Cantidad',
    seg_th_hombres:    'Hombres',
    seg_th_mujeres:    'Mujeres',
    seg_chart_sexo:    'Distribución por Sexo',
    th_mes_com:        'Mes Comisión',
    doc_th_titulo:     'Título',
    doc_lbl_titulo:    'Título',
    btn_nuevo_doc:     '<span>✦</span> Nuevo documento',
    toast_doc_saved:   'Documento guardado',
    toast_doc_deleted: 'Documento eliminado',
    confirm_del_doc:   '¿Eliminar el documento',
  },
  val: {
    login_sub:     'Accés per a APB — Regidoria de Benestar Social',
    login_footer:  'La sessió dura 8 hores · Token xifrat JWT',
    lbl_usuario:   'Usuari del departament',
    lbl_password:  'Contrasenya',
    btn_login:     'Iniciar sessió',
    btn_logout:    'Tancar sessió',
    view_title:    'Menjar a Casa',
    itab_usuarios:  '👥 Usuaris',
    itab_facturas:  '🧾 Factures',
    itab_comisiones:'📋 Comissions',
    stat_total:    'Total casos',
    stat_activos:  'Actius',
    stat_bajas:    'Donats de baixa',
    stat_zonas:    'Zones amb casos',
    stat_hombres:  'Homes',
    stat_mujeres:  'Dones',
    comision_total: 'Total comissions',
    stat_tramite:   'En tràmit',
    stat_aprobadas: 'Aprovades',
    app_name:          'APBApp',
    itab_usuarios:     'Usuaris',
    itab_facturas:     'Factures',
    itab_comisiones:   'Comissions',
    btn_nuevo:         '+ Nou Cas',
    btn_nuevo_comision: '+ Nova Comissió',
    lbl_zona:          'Zona:',
    lbl_mes:           'Mes:',
    zona_todas:        'Totes',
    sip_search_placeholder: 'Buscar per SIP…',
    th_nombre:        'Cognoms, Nom',
    th_zona:          'Zona',
    th_edad:          'Edat',
    th_sexo:          'Sexe',
    th_telefono:      'Telèfon',
    th_renov:         'Mes Renov.',
    th_alta:          'F. Alta',
    th_estado:        'Estat',
    th_estado_comision: 'Estat',
    loading:       'Carregant casos…',
    btn_pdf:       '<span>📊</span> Generar Informe PDF',
    pdf_activos:   '📋 Tots els casos actius',
    pdf_renov:     '📅 Renovació del mes actual',
    btn_nuevo:     '<span>✦</span> Nou cas',
    btn_nuevo_comision: '<span>✦</span> Nova comissió',
    btn_aprobar:   '✓ Aprovar i crear usuari',
    lbl_apellidos: 'Cognoms <span class="req">*</span>',
    lbl_nombre:    'Nom <span class="req">*</span>',
    lbl_dni:       'DNI',
    lbl_sip:       'SIP <span class="field-hint-inline">(8 dígits)</span>',
    hint_dni:      '8 dígits + 1 lletra',
    hint_sip_inline: '(8 dígits)',
    lbl_zona_field:'Zona',
    lbl_rango_edad:"Rang d'edat",
    opt_menor_60:  '< 60 anys',
    opt_60_65:     '60-65 anys',
    opt_mayor_65:  '> 65 anys',
    lbl_sexo:      'Sexe',
    lbl_telefono:  'Telèfon',
    lbl_renov:     'Mes de renovació',
    lbl_alta:      "Data d'alta",
    lbl_baja:      'Data de baixa',
    lbl_direccion: 'Adreça',
    lbl_estado:    'Estat del cas',
    lbl_estado_comision: 'Estat de la comissió',
    lbl_obs:       'Observacions / Notes',
    btn_eliminar:  '🗑️ Eliminar',
    btn_cancelar:  'Cancel·lar',
    btn_guardar:   'Guardar',
    modal_new:     'Nou Cas',
    modal_edit:    'Editar Cas',
    modal_new_com: 'Nova Comissió',
    modal_edit_com:'Editar Comissió',
    modal_sub_new: 'Emplena les dades',
    sex_hombre:    'Home',
    sex_mujer:     'Dona',
    sex_no_define: 'No es definix',
    badge_activo:  '● Actiu',
    badge_baja:    '○ Baixa',
    badge_tramite: '◎ En tràmit',
    badge_aprobado:'✓ Aprovat',
    badge_denegado:'✗ Denegat',
    badge_tramite_opt:  'En tràmit',
    badge_aprobado_opt: 'Aprovat',
    badge_denegado_opt: 'Denegat',
    empty_no_data: 'No hi ha registres.',
    empty_no_filter:'Sense resultats per al filtre aplicat.',
    toggle_activo: 'Actiu',
    toggle_baja:   'Donat de baixa',
    toast_saved:   'Guardat correctament',
    toast_deleted: 'Eliminat',
    toast_load_err:'Error en carregar dades',
    toast_pdf_ok:  'PDF descarregat',
    toast_pdf_err: 'Error en generar PDF',
    toast_approved:"Comissió aprovada — usuari creat",
    confirm_del:   'Eliminar registre de',
    confirm_aprobar: "Aprovar la comissió de",
    login_empty:   'Introdueix usuari i contrasenya',
    login_verify:  'Verificant...',
    pdf_generating:'<span>⏳</span> Generant...',
    val_required:  'Camps obligatoris que falten',
    val_dni_or_sip:"Has d'introduir almenys DNI o SIP",
    val_dni_bad:   'El DNI ha de tindre 8 dígits i 1 lletra (ex: 12345678X)',
    val_sip_bad:       'SIP incorrecte (8 dígits)',
    chart_edad_title:  'Distribució per Edat',
    chart_sexo_title:  'Distribució per Gènere',
    chart_estado_title: 'Distribució per Estat',
    chart_estado_com_title: 'Estat de Tramitació',
    welcome:       'Benvingut,',
    opt_no_asignar:'— Sense assignar —',
    opt_no_sexo:   '— No especificat —',
    facturas_title:'Factures anuals',
    facturas_anio: 'Any:',
    th_mes:        'Mes',
    th_num_casos:  'Nº Casos',
    th_cuantia:    'Quantia (€)',
    th_pdf_adjunto:'PDF Adjunt',
    btn_subir_pdf: 'Pujar PDF',
    btn_ver_pdf:   'Veure PDF',
    btn_cambiar_pdf:'Canviar',
    pdf_fact_anual:    '📋 Facturació de l\'any seleccionat',
    pdf_com_tramite:   '📋 Comissions en tràmit',
    toast_pdf_facturas_err: 'Error en generar PDF de factures',
    toast_pdf_com_err:      'Error en generar PDF de comissions',
    toast_pdf_seg_err:      'Error en generar PDF de seguiment',
    itab_seguimiento:  '📊 Seguiment',
    itab_documentacion:'📁 Documentació',
    seg_title:         'Seguiment anual',
    seg_entrevistas:   '🗣 Entrevistes',
    seg_visitas:       '🚪 Visites',
    seg_informes:      '📄 Informes',
    seg_th_cantidad:   'Quantitat',
    seg_th_hombres:    'Homes',
    seg_th_mujeres:    'Dones',
    seg_chart_sexo:    'Distribució per Sexe',
    th_mes_com:        'Mes Comissió',
    doc_th_titulo:     'Títol',
    doc_lbl_titulo:    'Títol',
    btn_nuevo_doc:     '<span>✦</span> Nou document',
    btn_quitar_pdf:    'Eliminar PDF',
    confirm_quitar_pdf: 'Segur que vols eliminar el PDF adjunt?',
    toast_doc_saved:   'Document guardat',
    toast_doc_deleted: 'Document eliminat',
    toast_pdf_deleted: 'PDF eliminat correctament',
    confirm_del_doc:   'Eliminar el document',
  },
};

function t(key) { return I18N[state.lang]?.[key] ?? I18N.es[key] ?? key; }

function applyI18n() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const text = t(key);
    if (text !== undefined) el.innerHTML = text;
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    const text = t(key);
    if (text !== undefined) el.placeholder = text;
  });
  document.querySelectorAll('.sort-btn').forEach(btn => {
    const key = btn.getAttribute('data-i18n');
    const dirEl = btn.querySelector('.sort-dir');
    if (key && dirEl) btn.innerHTML = t(key) + ' ' + dirEl.outerHTML;
  });
  const langBtn = g('btn-lang');
  if (langBtn) langBtn.textContent = state.lang === 'es' ? 'ES' : 'VAL';
}

// ── Estado global ─────────────────────────────────────────────
const state = {
  // Usuarios
  casos:       [],
  editingId:   null,
  sortBy:      'nombre',
  sortDir:     'asc',
  filterZona:  null,
  sipSearch:   '',
  // Comisiones
  comisiones:          [],
  editingComisionId:   null,
  filterComisionZona:  null,
  filterComisionMes:   null,
  sipSearchComision:   '',
  // Facturas
  facturas:    [],
  facturasAnio: new Date().getFullYear(),
  // Seguimiento
  seguimientos:  [],
  segAnio:       new Date().getFullYear(),
  segTab:        'entrevista',
  // Documentación
  docs:          [],
  editingDocId:  null,
  // UI
  innerTab:    'usuarios',
  modalMode:   'usuario',   // 'usuario' | 'comision'
  // Auth / prefs
  token:     localStorage.getItem('apbapp_token'),
  deptName:  localStorage.getItem('apbapp_dept'),
  lang:      localStorage.getItem('apbapp_lang') || 'es',
};

// ── Utilidades ────────────────────────────────────────────────

function g(id) { return document.getElementById(id); }

async function api(method, path, body = null) {
  const headers = { 'Content-Type': 'application/json' };
  if (state.token) headers['Authorization'] = `Bearer ${state.token}`;
  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(path, opts);
  if (res.status === 401) { logout(); throw new Error('Sesión expirada'); }
  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || `Error ${res.status}`);
  return data;
}

function formatMes(val) {
  if (!val) return '—';
  const [year, month] = val.split('-').map(Number);
  const meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
  return `${meses[month - 1]} ${year}`;
}

function formatFecha(val) {
  if (!val) return '—';
  const [y, m, d] = val.split('-');
  return `${d}/${m}/${y}`;
}

function esc(str) {
  if (!str) return '';
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function highlightSIP(text, query) {
  if (!query || !text) return `<span>${esc(text)}</span>`;
  const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return esc(text).replace(
    new RegExp(`(${escapedQuery})`, 'gi'),
    '<mark class="sip-highlight">$1</mark>'
  );
}

function rangoEdadLabel(v) {
  if (v === 'menor_60') return `<span class="edad-badge edad-menor60">${t('opt_menor_60')}</span>`;
  if (v === '60_65')    return `<span class="edad-badge edad-6065">${t('opt_60_65')}</span>`;
  if (v === 'mayor_65') return `<span class="edad-badge edad-mayor65">${t('opt_mayor_65')}</span>`;
  return '—';
}

// ── Validación DNI / SIP ─────────────────────────────────────

const RE_DNI = /^\d{8}[A-Za-z]$/;
const RE_SIP = /^\d{8}$/;

function validarDniSip(dni, sip) {
  const errors = [];
  if (!dni && !sip) errors.push('val_dni_or_sip');
  if (dni && !RE_DNI.test(dni)) errors.push('val_dni_bad');
  if (sip && !RE_SIP.test(sip)) errors.push('val_sip_bad');
  return errors.length ? errors : null;
}

// ── Autenticación ─────────────────────────────────────────────

async function onLoginSubmit(e) {
  e.preventDefault();
  const user = g('login-user').value.trim();
  const pass = g('login-pass').value.trim();
  const errEl = g('login-error');
  const btn   = g('login-btn');

  if (!user || !pass) {
    errEl.classList.remove('hidden');
    g('login-error-msg').textContent = t('login_empty');
    return;
  }

  btn.disabled = true;
  btn.textContent = t('login_verify');
  errEl.classList.add('hidden');

  try {
    const data = await api('POST', '/auth/login', { username: user, password: pass });
    state.token    = data.access_token;
    state.deptName = data.dept_name;
    localStorage.setItem('apbapp_token', data.access_token);
    localStorage.setItem('apbapp_dept', data.dept_name);
    initApp();
    toast(`${t('welcome')} ${state.deptName}`, 'success');
  } catch (err) {
    errEl.classList.remove('hidden');
    g('login-error-msg').textContent = err.message;
    btn.disabled = false;
    btn.textContent = t('btn_login');
  }
}

function logout() {
  state.token = null;
  state.deptName = null;
  localStorage.removeItem('apbapp_token');
  localStorage.removeItem('apbapp_dept');
  g('main-app').classList.add('hidden');
  g('login-screen').classList.remove('hidden');
  g('login-form').reset();
  g('login-btn').disabled = false;
  g('login-btn').textContent = t('btn_login');
}

function initApp() {
  if (!state.token) {
    g('login-screen').classList.remove('hidden');
    g('main-app').classList.add('hidden');
    return;
  }
  g('login-screen').classList.add('hidden');
  g('main-app').classList.remove('hidden');
  cargarCasos().catch(() => toast(t('toast_load_err'), 'error'));
  initFacturasAnio();
  initSegAnio();
}

// ── Inner tabs ────────────────────────────────────────────────

function switchInnerTab(tab) {
  state.innerTab = tab;
  document.querySelectorAll('.inner-tab').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.itab === tab);
  });
  document.querySelectorAll('.inner-tab-panel').forEach(panel => {
    panel.classList.toggle('hidden', panel.id !== `itab-${tab}`);
  });

  if (tab === 'usuarios' && state.casos.length === 0) {
    cargarCasos().catch(() => toast(t('toast_load_err'), 'error'));
  }
  if (tab === 'comisiones') {
    cargarComisiones().catch(() => toast(t('toast_load_err'), 'error'));
  }
  if (tab === 'facturas') {
    cargarFacturas();
  }
  if (tab === 'seguimiento') {
    cargarSeguimientos();
  }
  if (tab === 'documentacion') {
    cargarDocs();
  }
}

// ── API: CRUD Casos ───────────────────────────────────────────

async function cargarCasos() {
  state.casos = await api('GET', '/mayor-a-casa/casos/');
  renderTabla();
  renderStats();
  renderStats();
}

async function crearCaso(datos) {
  await api('POST', '/mayor-a-casa/casos/', datos);
  await cargarCasos();
}

async function actualizarCaso(id, datos) {
  await api('PATCH', `/mayor-a-casa/casos/${id}`, datos);
  await cargarCasos();
}

async function eliminarCaso(id) {
  await api('DELETE', `/mayor-a-casa/casos/${id}`);
  await cargarCasos();
}

// ── API: CRUD Comisiones ──────────────────────────────────────

async function cargarComisiones() {
  state.comisiones = await api('GET', '/mayor-a-casa/comisiones/');
  renderComisiones();
  renderStatsComisiones();
}

async function crearComision(datos) {
  await api('POST', '/mayor-a-casa/comisiones/', datos);
  await cargarComisiones();
}

async function actualizarComision(id, datos) {
  await api('PATCH', `/mayor-a-casa/comisiones/${id}`, datos);
  await cargarComisiones();
}

async function eliminarComision(id) {
  await api('DELETE', `/mayor-a-casa/comisiones/${id}`);
  await cargarComisiones();
}

async function eliminarPdfFactura(id) {
  await api('DELETE', `/mayor-a-casa/facturas/${id}/pdf`);
  await cargarFacturas();
}

async function aprobarComision(id) {
  const caso = await api('POST', `/mayor-a-casa/comisiones/${id}/aprobar`);
  await cargarComisiones();
  await cargarCasos();
  cerrarModal();
  toast(t('toast_approved'), 'success');
  // Switch to usuarios to show new entry
  switchInnerTab('usuarios');
  return caso;
}

// ── API: CRUD Facturas ────────────────────────────────────────

async function cargarFacturas() {
  try {
    state.facturas = await api('GET', `/mayor-a-casa/facturas/?anio=${state.facturasAnio}`);
    renderFacturas();
    renderStatsFacturas();
  } catch {
    toast(t('toast_load_err'), 'error');
  }
}

function renderStatsFacturas() {
  const inputs = document.querySelectorAll('.factura-input');
  let totalCasos = 0;
  let totalCuantia = 0;
  inputs.forEach(input => {
    const val = parseFloat(input.value) || 0;
    if (input.dataset.field === 'num_casos') totalCasos += val;
    else if (input.dataset.field === 'cuantia') totalCuantia += val;
  });

  if (g('stat-fact-casos'))   g('stat-fact-casos').textContent   = totalCasos;
  if (g('stat-fact-cuantia')) g('stat-fact-cuantia').textContent = totalCuantia.toFixed(2) + ' €';
}

async function guardarFactura(anio, mes, datos) {
  try {
    const result = await api('PUT', '/mayor-a-casa/facturas/', { anio, mes, ...datos });
    const idx = state.facturas.findIndex(f => f.anio === anio && f.mes === mes);
    if (idx >= 0) state.facturas[idx] = result;
    else state.facturas.push(result);
    return result;
  } catch (err) {
    toast(err.message, 'error');
    return null;
  }
}

async function subirPdfFactura(facturaId, file) {
  const formData = new FormData();
  formData.append('file', file);
  const headers = {};
  if (state.token) headers['Authorization'] = `Bearer ${state.token}`;
  const res = await fetch(`/mayor-a-casa/facturas/${facturaId}/pdf`, {
    method: 'POST', headers, body: formData,
  });
  if (!res.ok) throw new Error('Error al subir PDF');
  return res.json();
}

// ── Seguimiento ───────────────────────────────────────────────

async function cargarSeguimientos() {
  try {
    state.seguimientos = await api('GET', `/mayor-a-casa/seguimientos/?anio=${state.segAnio}`);
    renderSeguimientos();
  } catch {
    toast(t('toast_load_err'), 'error');
  }
}

async function guardarSeguimiento(tipo, anio, mes, datos) {
  try {
    const result = await api('PUT', '/mayor-a-casa/seguimientos/', { tipo, anio, mes, ...datos });
    const idx = state.seguimientos.findIndex(s => s.tipo === tipo && s.anio === anio && s.mes === mes);
    if (idx >= 0) state.seguimientos[idx] = result;
    else state.seguimientos.push(result);
    renderSeguimientoChart(tipo);
  } catch (err) { toast(err.message, 'error'); }
}

function initSegAnio() {
  const sel = g('seg-anio');
  if (!sel) return;
  const cur = new Date().getFullYear();
  sel.innerHTML = '';
  for (let y = cur + 2; y >= cur - 4; y--) {
    const opt = document.createElement('option');
    opt.value = y; opt.textContent = y;
    if (y === state.segAnio) opt.selected = true;
    sel.appendChild(opt);
  }
  sel.addEventListener('change', () => {
    state.segAnio = parseInt(sel.value);
    cargarSeguimientos();
  });
}

function renderSeguimientos() {
  ['entrevista','visita','informe'].forEach(tipo => renderSeguimientoTabla(tipo));
  ['entrevista','visita','informe'].forEach(tipo => renderSeguimientoChart(tipo));
}

function renderSeguimientoTabla(tipo) {
  const tbody = g(`tbody-seg-${tipo}`);
  if (!tbody) return;
  const anio  = state.segAnio;
  const meses = state.lang === 'val' ? MESES_VAL : MESES_ES;

  tbody.innerHTML = meses.map((mesNom, i) => {
    const mes = i + 1;
    const row = state.seguimientos.find(s => s.tipo === tipo && s.anio === anio && s.mes === mes);
    const rowId   = row?.id ?? '';
    const cant    = row?.cantidad ?? '';
    const hombres = row?.hombres  ?? '';
    const mujeres = row?.mujeres  ?? '';
    return `
      <tr>
        <td class="td-name">${mesNom}</td>
        <td><input type="number" min="0" class="seg-input table-input" data-tipo="${tipo}" data-anio="${anio}" data-mes="${mes}" data-field="cantidad"  data-sid="${rowId}" value="${cant}"    placeholder="—"></td>
        <td><input type="number" min="0" class="seg-input table-input" data-tipo="${tipo}" data-anio="${anio}" data-mes="${mes}" data-field="hombres"   data-sid="${rowId}" value="${hombres}" placeholder="—"></td>
        <td><input type="number" min="0" class="seg-input table-input" data-tipo="${tipo}" data-anio="${anio}" data-mes="${mes}" data-field="mujeres"   data-sid="${rowId}" value="${mujeres}" placeholder="—"></td>
      </tr>`;
  }).join('');

  tbody.querySelectorAll('.seg-input').forEach(input => {
    input.addEventListener('change', async e => {
      const { tipo: tp, anio: a, mes: m, field } = e.target.dataset;
      const raw = e.target.value;
      const value = raw === '' ? null : parseInt(raw);
      await guardarSeguimiento(tp, parseInt(a), parseInt(m), { [field]: value });
    });
  });
}

function renderSeguimientoChart(tipo) {
  const canvas = g(`chart-seg-${tipo}`);
  const legend = g(`chart-legend-seg-${tipo}`);
  if (!canvas || !legend) return;
  const anio = state.segAnio;
  const rows = state.seguimientos.filter(s => s.tipo === tipo && s.anio === anio);
  const totalH = rows.reduce((acc, r) => acc + (r.hombres || 0), 0);
  const totalM = rows.reduce((acc, r) => acc + (r.mujeres || 0), 0);
  const total  = totalH + totalM;
  _drawDonut(canvas, legend, [
    { label: t('seg_th_hombres'), color: '#f59e0b', count: totalH },
    { label: t('seg_th_mujeres'), color: '#9333ea', count: totalM },
  ], total);
}

// ── Documentación ─────────────────────────────────────────────

async function cargarDocs() {
  try {
    state.docs = await api('GET', '/mayor-a-casa/documentacion/');
    renderDocs();
  } catch {
    toast(t('toast_load_err'), 'error');
  }
}

async function crearDoc(titulo) {
  const doc = await api('POST', '/mayor-a-casa/documentacion/', { titulo });
  state.docs.push(doc);
  renderDocs();
  return doc;
}

async function actualizarDoc(id, datos) {
  const doc = await api('PATCH', `/mayor-a-casa/documentacion/${id}`, datos);
  const idx = state.docs.findIndex(d => d.id === id);
  if (idx >= 0) state.docs[idx] = doc;
  renderDocs();
}

async function eliminarDoc(id) {
  await api('DELETE', `/mayor-a-casa/documentacion/${id}`);
  state.docs = state.docs.filter(d => d.id !== id);
  renderDocs();
}

async function subirPdfDoc(docId, file) {
  const formData = new FormData();
  formData.append('file', file);
  const headers = {};
  if (state.token) headers['Authorization'] = `Bearer ${state.token}`;
  const res = await fetch(`/mayor-a-casa/documentacion/${docId}/pdf`, {
    method: 'POST', headers, body: formData,
  });
  if (!res.ok) throw new Error('Error al subir PDF');
  return res.json();
}

async function eliminarPdfDoc(id) {
  await api('DELETE', `/mayor-a-casa/documentacion/${id}/pdf`);
  await cargarDocs();
}

function renderDocs() {
  const tbody = g('tbody-docs');
  if (!tbody) return;
  if (!state.docs.length) {
    tbody.innerHTML = `<tr><td colspan="3" class="empty-cell">${t('empty_no_data')}</td></tr>`;
    return;
  }
  tbody.innerHTML = state.docs.map(doc => `
    <tr data-doc-id="${doc.id}">
      <td><input class="doc-titulo-input" data-id="${doc.id}" value="${esc(doc.titulo)}" /></td>
      <td class="td-pdf-cell">
        ${doc.pdf_filename
          ? `<div class="pdf-btn-group">
               <a class="btn btn-ghost btn-sm" href="/static/uploads/documentacion/${doc.pdf_filename}" target="_blank">📄 ${t('btn_ver_pdf')}</a>
               <button class="btn btn-ghost btn-sm delete-doc-pdf-btn" data-id="${doc.id}" title="${t('btn_quitar_pdf')}">🗑️</button>
             </div>`
          : ''}
        <label class="btn btn-ghost btn-sm upload-label">
          📎 ${doc.pdf_filename ? t('btn_cambiar_pdf') : t('btn_subir_pdf')}
          <input type="file" accept="application/pdf" class="upload-doc-pdf hidden" data-doc-id="${doc.id}">
        </label>
      </td>
      <td class="td-actions">
        <button class="btn-icon delete-doc-btn" data-id="${doc.id}" title="Eliminar">🗑</button>
      </td>
    </tr>
  `).join('');

  tbody.querySelectorAll('.delete-doc-pdf-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      if (confirm(t('confirm_quitar_pdf'))) {
        try {
          await eliminarPdfDoc(parseInt(btn.dataset.id));
          toast(t('toast_pdf_deleted'), 'info');
        } catch (err) { toast(err.message, 'error'); }
      }
    });
  });

  tbody.querySelectorAll('.doc-titulo-input').forEach(input => {
    input.addEventListener('change', async e => {
      const id = parseInt(e.target.dataset.id);
      const titulo = e.target.value.trim();
      if (!titulo) return;
      try { await actualizarDoc(id, { titulo }); } catch (err) { toast(err.message, 'error'); }
    });
  });

  tbody.querySelectorAll('.upload-doc-pdf').forEach(input => {
    input.addEventListener('change', async e => {
      const file = e.target.files[0];
      if (!file) return;
      const docId = parseInt(e.target.dataset.docId);
      try {
        await subirPdfDoc(docId, file);
        await cargarDocs();
        toast('PDF subido correctamente', 'success');
      } catch (err) { toast(err.message, 'error'); }
    });
  });

  tbody.querySelectorAll('.delete-doc-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = parseInt(btn.dataset.id);
      const doc = state.docs.find(d => d.id === id);
      if (doc && confirm(`${t('confirm_del_doc')} "${doc.titulo}"?`)) {
        try {
          await eliminarDoc(id);
          toast(t('toast_doc_deleted'), 'info');
        } catch (err) { toast(err.message, 'error'); }
      }
    });
  });
}

// ── Estadísticas Usuarios ─────────────────────────────────────

function renderStats() {
  let list = [...state.casos];
  if (state.filterZona !== null) list = list.filter(c => c.zona === state.filterZona);
  
  // Chart 1: Estado (Activos / Bajas)
  const total = list.length;
  const activos = list.filter(c => c.activo).length;
  const bajas = total - activos;
  _drawDonut(g('chart-estado'), g('chart-legend-estado'), [
    { label: 'Activo', color: '#10b981', count: activos },
    { label: 'Baja',   color: '#64748b', count: bajas }
  ], total);

  // Chart 2: Sexo
  _drawDonut(g('chart-sexo'), g('chart-legend-sexo'), [
    { label: t('sex_hombre'),    color: '#f59e0b', count: list.filter(c => c.sexo === 'hombre').length },
    { label: t('sex_mujer'),     color: '#9333ea', count: list.filter(c => c.sexo === 'mujer').length },
    { label: t('sex_no_define'), color: '#94a3b8', count: list.filter(c => c.sexo === 'no_define' || !c.sexo).length }
  ], total);

  // Chart 3: Edad
  _drawDonut(g('chart-edad'), g('chart-legend-edad'), [
    { label: t('opt_menor_60'), color: '#f59e0b', count: list.filter(c => c.rango_edad === 'menor_60').length },
    { label: t('opt_60_65'),    color: '#3b82f6', count: list.filter(c => c.rango_edad === '60_65').length },
    { label: t('opt_mayor_65'), color: '#06b6d4', count: list.filter(c => c.rango_edad === 'mayor_65').length },
    { label: 'N/D',             color: '#334155', count: list.filter(c => !c.rango_edad).length }
  ], total);
}

function renderStatsComisiones() {
  let list = [...state.comisiones];
  if (state.filterComisionZona !== null) list = list.filter(c => c.zona === state.filterComisionZona);
  if (state.filterComisionMes)           list = list.filter(c => c.mes_comision === state.filterComisionMes);
  
  const total = list.length;

  // Chart 1: Estado de Tramitación
  _drawDonut(g('chart-estado-com'), g('chart-legend-estado-com'), [
    { label: 'Trámite',  color: '#f59e0b', count: list.filter(c => c.estado === 'en_tramite').length },
    { label: 'Aprobado', color: '#10b981', count: list.filter(c => c.estado === 'aprobado').length },
    { label: 'Denegado', color: '#ef4444', count: list.filter(c => c.estado === 'denegado').length }
  ], total);

  // Chart 2: Sexo
  _drawDonut(g('chart-sexo-com'), g('chart-legend-sexo-com'), [
    { label: t('sex_hombre'),    color: '#f59e0b', count: list.filter(c => c.sexo === 'hombre').length },
    { label: t('sex_mujer'),     color: '#9333ea', count: list.filter(c => c.sexo === 'mujer').length },
    { label: t('sex_no_define'), color: '#94a3b8', count: list.filter(c => c.sexo === 'no_define' || !c.sexo).length }
  ], total);

  // Chart 3: Edad
  _drawDonut(g('chart-edad-com'), g('chart-legend-edad-com'), [
    { label: t('opt_menor_60'), color: '#f59e0b', count: list.filter(c => c.rango_edad === 'menor_60').length },
    { label: t('opt_60_65'),    color: '#3b82f6', count: list.filter(c => c.rango_edad === '60_65').length },
    { label: t('opt_mayor_65'), color: '#06b6d4', count: list.filter(c => c.rango_edad === 'mayor_65').length },
    { label: 'N/D',             color: '#334155', count: list.filter(c => !c.rango_edad).length }
  ], total);
}

function _drawDonut(canvas, legend, data, total) {
  const ctx = canvas.getContext('2d');
  const w = canvas.width, h = canvas.height;
  ctx.clearRect(0, 0, w, h);
  const cx = w/2, cy = h/2, r = Math.min(w,h)/2-4, innerR = r*0.55;

  if (total === 0) {
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, 2*Math.PI);
    ctx.fillStyle = '#2d3a4d'; ctx.fill();
  } else {
    let angle = -Math.PI/2;
    data.forEach(d => {
      if (d.count === 0) return;
      const slice = (d.count / total) * 2 * Math.PI;
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.arc(cx, cy, r, angle, angle + slice); ctx.closePath();
      ctx.fillStyle = d.color; ctx.fill();
      angle += slice;
    });
  }
  ctx.beginPath(); ctx.arc(cx, cy, innerR, 0, 2*Math.PI);
  const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
  ctx.fillStyle = isDark ? '#18212f' : '#ffffff'; ctx.fill();
  ctx.fillStyle = isDark ? '#e8eef5' : '#111827';
  ctx.font = `bold ${Math.round(r*0.38)}px Inter,sans-serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(String(total), cx, cy);

  if (legend) {
    legend.innerHTML = data.filter(d => d.count > 0).map(d => {
      const pct = total ? Math.round((d.count / total) * 100) : 0;
      return `<div class="legend-item">
        <span class="legend-dot" style="background:${d.color}"></span>
        <span class="legend-label">${d.label}</span>
        <span class="legend-val">${d.count} <em>${pct}%</em></span>
      </div>`;
    }).join('');
  }
}

// ── Filtrado y ordenación (usuarios) ─────────────────────────

function getFilteredSorted() {
  let list = [...state.casos];
  if (state.filterZona !== null) {
    list = list.filter(c => c.zona === state.filterZona);
  }
  if (state.sipSearch) {
    const q = state.sipSearch.toLowerCase();
    list = list.filter(c => c.sip && c.sip.toLowerCase().includes(q));
  }
  list.sort((a, b) => {
    if (state.sortBy === 'nombre') {
      const sa = `${a.apellidos || ''} ${a.nombre || ''}`;
      const sb = `${b.apellidos || ''} ${b.nombre || ''}`;
      const cmp = sa.localeCompare(sb, 'es', { sensitivity: 'base' });
      return state.sortDir === 'asc' ? cmp : -cmp;
    }
    let va, vb;
    if (state.sortBy === 'fecha_alta') {
      if (!a.fecha_alta && !b.fecha_alta) return 0;
      if (!a.fecha_alta) return 1; if (!b.fecha_alta) return -1;
      va = a.fecha_alta; vb = b.fecha_alta;
    } else if (state.sortBy === 'renovacion') {
      if (!a.mes_renovacion && !b.mes_renovacion) return 0;
      if (!a.mes_renovacion) return 1; if (!b.mes_renovacion) return -1;
      va = a.mes_renovacion; vb = b.mes_renovacion;
    } else if (state.sortBy === 'activo') {
      va = a.activo ? 0 : 1; vb = b.activo ? 0 : 1;
    }
    if (va < vb) return state.sortDir === 'asc' ? -1 : 1;
    if (va > vb) return state.sortDir === 'asc' ? 1 : -1;
    return 0;
  });
  return list;
}

function updateSortUI() {
  document.querySelectorAll('.sort-btn').forEach(btn => {
    const key = btn.dataset.sort;
    const dirEl = btn.querySelector('.sort-dir');
    const isActive = key === state.sortBy;
    btn.classList.toggle('active', isActive);
    if (dirEl) dirEl.textContent = !isActive ? '↕' : (state.sortDir === 'asc' ? '↑' : '↓');
  });
}

// ── Tabla Usuarios ────────────────────────────────────────────

function renderTabla() {
  const tbody = g('tbody-casos');
  if (!tbody) return;
  const list = getFilteredSorted();

  const countEl = g('results-count');
  if (countEl) {
    const total = state.casos.length;
    countEl.textContent = list.length === total
      ? `${total} caso${total !== 1 ? 's' : ''}`
      : `${list.length} de ${total}`;
  }

  const sexLabels = { hombre: t('sex_hombre'), mujer: t('sex_mujer'), no_define: t('sex_no_define') };

  if (!state.casos.length) {
    tbody.innerHTML = `<tr><td colspan="11" class="empty-cell">${t('empty_no_data')}</td></tr>`;
    return;
  }
  if (!list.length) {
    tbody.innerHTML = `<tr><td colspan="11" class="loading-cell"><div class="spinner"></div></td></tr>`;
    return;
  }

  tbody.innerHTML = list.map(c => `
    <tr data-id="${c.id}">
      <td class="td-name" style="text-align: left;"><strong>${esc(c.apellidos)}</strong>,&nbsp;${esc(c.nombre)}</td>
      <td style="text-align: left;">${esc(c.dni) || '—'}</td>
      <td style="text-align: left;">${state.sipSearch ? highlightSIP(c.sip, state.sipSearch) : (esc(c.sip) || '—')}</td>
      <td style="text-align: left;">${c.zona ? `<span class="zona-badge" data-zona="${c.zona}">Zona ${c.zona}</span>` : '—'}</td>
      <td style="text-align: left;">${rangoEdadLabel(c.rango_edad)}</td>
      <td style="text-align: left;">${sexLabels[c.sexo] || '—'}</td>
      <td style="text-align: left;">${esc(c.telefono) || '—'}</td>
      <td style="text-align: left;">${formatMes(c.mes_renovacion)}</td>
      <td style="text-align: left;">${formatFecha(c.fecha_alta)}</td>
      <td style="text-align: left;"><span class="badge ${c.activo ? 'badge-activo' : 'badge-baja'}">${c.activo ? t('badge_activo') : t('badge_baja')}</span></td>
      <td class="td-actions" style="text-align: left;">
        <button class="btn-icon edit-btn" data-id="${c.id}" title="Editar">✏️</button>
        <button class="btn-icon delete-btn" data-id="${c.id}" title="Eliminar">🗑</button>
      </td>
    </tr>
  `).join('');

  tbody.querySelectorAll('tr[data-id]').forEach(row => {
    row.addEventListener('click', () => abrirModal(state.casos.find(c => c.id === parseInt(row.dataset.id))));
  });
  tbody.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      abrirModal(state.casos.find(c => c.id === parseInt(btn.dataset.id)));
    });
  });
  tbody.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const caso = state.casos.find(c => c.id === parseInt(btn.dataset.id));
      if (caso) confirmarEliminarCaso(caso);
    });
  });
}

// ── Tabla Comisiones ──────────────────────────────────────────

function getFilteredComisiones() {
  let list = [...state.comisiones];
  if (state.filterComisionZona !== null) {
    list = list.filter(c => c.zona === state.filterComisionZona);
  }
  if (state.filterComisionMes) {
    list = list.filter(c => c.mes_comision === state.filterComisionMes);
  }
  if (state.sipSearchComision) {
    const q = state.sipSearchComision.toLowerCase();
    list = list.filter(c => c.sip && c.sip.toLowerCase().includes(q));
  }
  return list.sort((a, b) =>
    `${a.apellidos || ''} ${a.nombre || ''}`.localeCompare(`${b.apellidos || ''} ${b.nombre || ''}`, 'es', { sensitivity: 'base' })
  );
}

function estadoBadge(estado) {
  const map = {
    en_tramite: `<span class="badge badge-tramite">${t('badge_tramite')}</span>`,
    aprobado:   `<span class="badge badge-aprobado">${t('badge_aprobado')}</span>`,
    denegado:   `<span class="badge badge-denegado">${t('badge_denegado')}</span>`,
  };
  return map[estado] || estado;
}

function renderComisiones() {
  const tbody = g('tbody-comisiones');
  if (!tbody) return;
  const list = getFilteredComisiones();
  const sexLabels = { hombre: t('sex_hombre'), mujer: t('sex_mujer'), no_define: t('sex_no_define') };

  if (!state.comisiones.length) {
    tbody.innerHTML = `<tr><td colspan="9" class="empty-cell">${t('empty_no_data')}</td></tr>`;
    return;
  }
  if (!list.length) {
    tbody.innerHTML = `<tr><td colspan="9" class="empty-cell">${t('empty_no_filter')}</td></tr>`;
    return;
  }

  tbody.innerHTML = list.map(c => `
    <tr data-id="${c.id}">
      <td class="td-name"><strong>${esc(c.apellidos)}</strong>,&nbsp;${esc(c.nombre)}</td>
      <td>${esc(c.dni) || '—'}</td>
      <td>${state.sipSearchComision ? highlightSIP(c.sip, state.sipSearchComision) : (esc(c.sip) || '—')}</td>
      <td>${c.zona ? `<span class="zona-badge" data-zona="${c.zona}">Zona ${c.zona}</span>` : '—'}</td>
      <td>${rangoEdadLabel(c.rango_edad)}</td>
      <td>${sexLabels[c.sexo] || '—'}</td>
      <td>${formatMes(c.mes_comision)}</td>
      <td>${estadoBadge(c.estado)}</td>
      <td class="td-actions">
        <button class="btn-icon edit-btn-c" data-id="${c.id}" title="Editar">✏️</button>
        <button class="btn-icon delete-btn-c" data-id="${c.id}" title="Eliminar">🗑</button>
      </td>
    </tr>
  `).join('');

  tbody.querySelectorAll('tr[data-id]').forEach(row => {
    row.addEventListener('click', () => {
      const com = state.comisiones.find(c => c.id === parseInt(row.dataset.id));
      if (com) abrirModal(com, 'comision');
    });
  });
  tbody.querySelectorAll('.edit-btn-c').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const com = state.comisiones.find(c => c.id === parseInt(btn.dataset.id));
      if (com) abrirModal(com, 'comision');
    });
  });
  tbody.querySelectorAll('.delete-btn-c').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const com = state.comisiones.find(c => c.id === parseInt(btn.dataset.id));
      if (com && confirm(`${t('confirm_del')} ${com.apellidos}?`)) {
        eliminarComision(com.id).then(() => toast(t('toast_deleted'), 'info')).catch(err => toast(err.message, 'error'));
      }
    });
  });
}

// ── Tabla Facturas ────────────────────────────────────────────

const MESES_ES  = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
const MESES_VAL = ['Gener','Febrer','Març','Abril','Maig','Juny','Juliol','Agost','Setembre','Octubre','Novembre','Desembre'];

function initFacturasAnio() {
  const sel = g('facturas-anio');
  if (!sel) return;
  const cur = new Date().getFullYear();
  sel.innerHTML = '';
  // Mostrar 2 años futuros y 4 pasados
  for (let y = cur + 2; y >= cur - 4; y--) {
    const opt = document.createElement('option');
    opt.value = y; opt.textContent = y;
    if (y === state.facturasAnio) opt.selected = true;
    sel.appendChild(opt);
  }
  sel.addEventListener('change', () => {
    state.facturasAnio = parseInt(sel.value);
    cargarFacturas();
  });
}

function renderFacturas() {
  const tbody = g('tbody-facturas');
  if (!tbody) return;
  const anio  = state.facturasAnio;
  const meses = state.lang === 'val' ? MESES_VAL : MESES_ES;

  tbody.innerHTML = meses.map((mesNom, i) => {
    const mes     = i + 1;
    const factura = state.facturas.find(f => f.anio === anio && f.mes === mes);
    const fId     = factura?.id ?? '';
    const numVal  = factura?.num_casos ?? '';
    const cuaVal  = factura?.cuantia   != null ? factura.cuantia : '';
    const hasPdf  = factura?.pdf_filename;

    return `
      <tr>
        <td class="td-name">${mesNom}</td>
        <td>
          <input type="number" min="0" class="factura-input table-input"
                 data-anio="${anio}" data-mes="${mes}" data-field="num_casos"
                 data-fid="${fId}" value="${numVal}" placeholder="—">
        </td>
        <td>
          <input type="number" min="0" step="0.01" class="factura-input table-input"
                 data-anio="${anio}" data-mes="${mes}" data-field="cuantia"
                 data-fid="${fId}" value="${cuaVal}" placeholder="—">
        </td>
        <td class="td-pdf-cell">
          ${hasPdf
            ? `
              <div class="pdf-btn-group">
                <a class="btn btn-ghost btn-sm" href="/static/uploads/facturas/${factura.pdf_filename}" target="_blank">📄 ${t('btn_ver_pdf')}</a>
                <button class="btn btn-ghost btn-sm delete-pdf-btn" data-fid="${fId}" title="${t('btn_quitar_pdf')}">🗑</button>
              </div>`
            : ''}
          <label class="btn btn-ghost btn-sm upload-label">
            📎 ${hasPdf ? t('btn_cambiar_pdf') : t('btn_subir_pdf')}
            <input type="file" accept="application/pdf" class="upload-pdf hidden"
                   data-anio="${anio}" data-mes="${mes}" data-fid="${fId}">
          </label>
        </td>
      </tr>`;
  }).join('');

  // Refresco del resumen en tiempo real al escribir
  tbody.querySelectorAll('.factura-input').forEach(input => {
    input.addEventListener('input', () => {
      renderStatsFacturas();
    });

    input.addEventListener('change', async e => {
      const { anio: a, mes: m, field } = e.target.dataset;
      const raw = e.target.value;
      const value = raw === '' ? null : parseFloat(raw);
      const result = await guardarFactura(parseInt(a), parseInt(m), { [field]: value });
      if (result && !e.target.dataset.fid) {
        // Propagate new factura id to all inputs in this row
        const row = e.target.closest('tr');
        row.querySelectorAll('[data-fid]').forEach(el => el.dataset.fid = result.id);
      }
    });
  });

  // Subir PDF
  tbody.querySelectorAll('.upload-pdf').forEach(input => {
    input.addEventListener('change', async e => {
      const file = e.target.files[0];
      if (!file) return;
      let fid = e.target.dataset.fid;
      if (!fid) {
        const { anio: a, mes: m } = e.target.dataset;
        const result = await guardarFactura(parseInt(a), parseInt(m), {});
        if (!result) return;
        fid = result.id;
        const row = e.target.closest('tr');
        row.querySelectorAll('[data-fid]').forEach(el => el.dataset.fid = result.id);
      }
      try {
        await subirPdfFactura(fid, file);
        await cargarFacturas();
        toast('PDF subido correctamente', 'success');
      } catch (err) { toast(err.message, 'error'); }
    });
  });

  // Eliminar PDF
  tbody.querySelectorAll('.delete-pdf-btn').forEach(btn => {
    btn.addEventListener('click', async e => {
      const fid = btn.dataset.fid;
      if (!fid) return;
      if (confirm(t('confirm_quitar_pdf'))) {
        try {
          await eliminarPdfFactura(fid);
          toast(t('toast_pdf_deleted'), 'success');
        } catch (err) { toast(err.message, 'error'); }
      }
    });
  });
}

// ── Tema claro/oscuro ─────────────────────────────────────────

function initTheme() {
  applyTheme(localStorage.getItem('apbapp_theme') || 'dark');
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('apbapp_theme', theme);
  const btn = g('btn-theme');
  if (btn) btn.textContent = theme === 'dark' ? '🌙' : '☀️';
  renderStats(); // re-render with correct background color
}

function toggleTheme() {
  applyTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
}

// ── Idioma ────────────────────────────────────────────────────

function toggleLang() {
  state.lang = state.lang === 'es' ? 'val' : 'es';
  localStorage.setItem('apbapp_lang', state.lang);
  applyI18n();
  renderTabla();
  renderStats();
  renderStats();
  renderComisiones();
  renderStatsComisiones();
  renderFacturas();
  renderSeguimientos();
  renderDocs();
}

// ── Modal (usuarios y comisiones) ─────────────────────────────

function abrirModal(item = null, mode = 'usuario') {
  state.modalMode = mode;
  const esComision = mode === 'comision';

  if (esComision) {
    state.editingComisionId = item ? item.id : null;
    state.editingId = null;
  } else {
    state.editingId = item ? item.id : null;
    state.editingComisionId = null;
  }

  g('modal-title').textContent    = item
    ? (esComision ? t('modal_edit_com') : t('modal_edit'))
    : (esComision ? t('modal_new_com')  : t('modal_new'));
  g('modal-subtitle').textContent = item
    ? `${item.apellidos}, ${item.nombre}`
    : t('modal_sub_new');

  g('f-mes-com-row').classList.toggle('hidden', !esComision);
  g('f-alta-row').classList.toggle('hidden', esComision);
  g('f-baja-row').classList.toggle('hidden', esComision);
  g('btn-eliminar').classList.toggle('hidden', !item);
  g('btn-aprobar').classList.toggle('hidden',
    !(esComision && item && item.estado !== 'aprobado'));

  // Show/hide mode-specific sections
  g('activo-group').style.display         = esComision ? 'none' : '';
  g('comision-estado-group').style.display = esComision ? '' : 'none';
  g('f-mes-com-row').style.display        = esComision ? '' : 'none';
  g('f-alta-row').style.display           = esComision ? 'none' : '';
  g('f-baja-row').style.display           = esComision ? 'none' : '';
  g('f-renov-row').style.display          = esComision ? 'none' : '';

  g('caso-form').reset();

  // Clear validation styles
  ['f-apellidos','f-nombre','f-dni','f-sip'].forEach(id => {
    const el = g(id); if (el) el.classList.remove('input-error');
  });
  const dniHint = g('dni-hint');
  if (dniHint) { dniHint.textContent = t('hint_dni'); dniHint.classList.remove('error'); }

  if (item) {
    g('f-apellidos').value   = item.apellidos || '';
    g('f-nombre').value      = item.nombre    || '';
    g('f-dni').value         = item.dni       || '';
    g('f-sip').value         = item.sip       || '';
    g('f-zona').value        = item.zona      || '';
    g('f-rango-edad').value  = item.rango_edad || '';
    g('f-sexo').value        = item.sexo      || '';
    g('f-tel').value         = item.telefono  || '';
    g('f-renov').value       = item.mes_renovacion || '';
    g('f-alta').value        = item.fecha_alta || '';
    g('f-baja').value        = item.fecha_baja || '';
    g('f-dir').value         = item.direccion  || '';
    g('f-obs').value         = item.observaciones || '';
    if (esComision) {
      g('f-estado-comision').value = item.estado || 'en_tramite';
      g('f-mes-com').value = item.mes_comision || '';
    } else {
      g('f-activo').checked = item.activo !== false;
      updateToggleLabel();
    }
  } else {
    g('f-renov').value = new Date().toISOString().slice(0, 7);
    g('f-alta').value  = new Date().toISOString().slice(0, 10);
    if (esComision) {
      g('f-estado-comision').value = 'en_tramite';
      g('f-mes-com').value = new Date().toISOString().slice(0, 7);
    } else {
      updateToggleLabel();
    }
  }

  g('modal-backdrop').classList.remove('hidden');
  g('modal-submit').disabled   = false;
  g('modal-submit').textContent = t('btn_guardar');
}

function cerrarModal() {
  g('modal-backdrop').classList.add('hidden');
  state.editingId = null;
  state.editingComisionId = null;
}

function updateToggleLabel() {
  const checked = g('f-activo').checked;
  g('toggle-label-text').textContent = checked ? t('toggle_activo') : t('toggle_baja');
  g('toggle-label-text').style.color = checked ? 'var(--success)' : 'var(--text-3)';
}

async function onFormSubmit(e) {
  e.preventDefault();
  const esComision = state.modalMode === 'comision';
  const dni      = g('f-dni').value.trim();
  const sip      = g('f-sip').value.trim();
  const apellidos = g('f-apellidos').value.trim();
  const nombre    = g('f-nombre').value.trim();

  ['f-apellidos','f-nombre','f-dni','f-sip'].forEach(id => {
    const el = g(id); if (el) el.classList.remove('input-error');
  });

  if (!apellidos || !nombre) {
    if (!apellidos) g('f-apellidos').classList.add('input-error');
    if (!nombre)    g('f-nombre').classList.add('input-error');
    toast(t('val_required'), 'error');
    return;
  }

  const valErrors = validarDniSip(dni, sip);
  if (valErrors) {
    if (valErrors.includes('val_dni_or_sip')) {
      g('f-dni').classList.add('input-error');
      g('f-sip').classList.add('input-error');
    }
    if (valErrors.includes('val_dni_bad')) g('f-dni').classList.add('input-error');
    if (valErrors.includes('val_sip_bad')) g('f-sip').classList.add('input-error');
    toast(t(valErrors[0]), 'error');
    return;
  }

  const baseData = {
    apellidos, nombre,
    dni: dni || null,
    sip: sip || null,
    zona:           g('f-zona').value   ? parseInt(g('f-zona').value) : null,
    rango_edad:     g('f-rango-edad').value || null,
    sexo:           g('f-sexo').value   || null,
    mes_renovacion: g('f-renov').value  || null,
    telefono:       g('f-tel').value.trim() || null,
    direccion:      g('f-dir').value.trim() || null,
    observaciones:  g('f-obs').value.trim() || null,
  };
  if (!esComision) {
    baseData.fecha_alta = g('f-alta').value || null;
    baseData.fecha_baja = g('f-baja').value || null;
  } else {
    baseData.mes_comision = g('f-mes-com').value || null;
  }

  g('modal-submit').disabled = true;

  try {
    if (esComision) {
      const newStatus = g('f-estado-comision').value;
      const prevStatus = state.editingComisionId ? state.comisiones.find(c => c.id === state.editingComisionId)?.estado : null;
      
      if (newStatus === 'aprobado' && prevStatus !== 'aprobado') {
        if (!confirm(t('confirm_aprobar') + ' ' + apellidos + ', ' + nombre + '?')) {
          g('modal-submit').disabled = false;
          return;
        }
      }
      const datos = { ...baseData, estado: newStatus };
      if (state.editingComisionId) await actualizarComision(state.editingComisionId, datos);
      else                          await crearComision(datos);
    } else {
      const datos = { ...baseData, activo: g('f-activo').checked };
      if (state.editingId) await actualizarCaso(state.editingId, datos);
      else                  await crearCaso(datos);
    }
    cerrarModal();
    toast(t('toast_saved'), 'success');
  } catch (err) {
    toast(err.message, 'error');
  } finally {
    g('modal-submit').disabled = false;
  }
}

function confirmarEliminarCaso(caso) {
  if (confirm(`${t('confirm_del')} ${caso.apellidos}?`)) {
    eliminarCaso(caso.id)
      .then(() => toast(t('toast_deleted'), 'info'))
      .catch(err => toast(err.message, 'error'));
  }
}

// ── Generar PDF ───────────────────────────────────────────────

async function descargarPDF(tipo = 'activos') {
  const btn      = g('btn-pdf');
  const btnArrow = g('btn-pdf-toggle');
  btn.disabled = true; btnArrow.disabled = true;
  btn.innerHTML = t('pdf_generating');

  let path = tipo === 'renovacion'
    ? '/mayor-a-casa/casos/informe/pdf/renovacion'
    : '/mayor-a-casa/casos/informe/pdf';

  const params = new URLSearchParams();
  if (state.filterZona) params.append('zona', state.filterZona);
  params.append('lang', state.lang);
  if (params.toString()) path += `?${params.toString()}`;

  try {
    const res = await fetch(path, { headers: { 'Authorization': `Bearer ${state.token}` } });
    if (!res.ok) throw new Error(t('toast_pdf_err'));
    const blob = await res.blob();
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href = url; a.download = `informe_${new Date().toISOString().slice(0,10)}.pdf`;
    a.click();
    toast(t('toast_pdf_ok'), 'success');
  } catch (err) { toast(err.message, 'error'); }
  finally {
    btn.disabled = false; btnArrow.disabled = false;
    btn.innerHTML = t('btn_pdf');
  }
}

// ── PDF Facturas ──────────────────────────────────────────────

async function descargarPDFFacturas() {
  const btn      = g('btn-pdf-facturas');
  const btnArrow = g('btn-pdf-facturas-toggle');
  btn.disabled = true; btnArrow.disabled = true;
  btn.innerHTML = t('pdf_generating');

  const params = new URLSearchParams({ anio: state.facturasAnio, lang: state.lang });
  try {
    const res = await fetch(`/mayor-a-casa/facturas/informe/pdf?${params}`,
      { headers: { 'Authorization': `Bearer ${state.token}` } });
    if (!res.ok) throw new Error(t('toast_pdf_facturas_err'));
    const blob = await res.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `facturas_${state.facturasAnio}.pdf`;
    a.click();
    toast(t('toast_pdf_ok'), 'success');
  } catch (err) { toast(err.message, 'error'); }
  finally {
    btn.disabled = false; btnArrow.disabled = false;
    btn.innerHTML = t('btn_pdf');
  }
}

// ── PDF Comisiones ────────────────────────────────────────────

async function descargarPDFComisiones() {
  const btn      = g('btn-pdf-comisiones');
  const btnArrow = g('btn-pdf-comisiones-toggle');
  btn.disabled = true; btnArrow.disabled = true;
  btn.innerHTML = t('pdf_generating');

  const params = new URLSearchParams({ lang: state.lang });
  if (state.filterComisionZona) params.append('zona', state.filterComisionZona);
  if (state.filterComisionMes)  params.append('mes',  state.filterComisionMes);

  try {
    const res = await fetch(`/mayor-a-casa/comisiones/informe/pdf?${params}`,
      { headers: { 'Authorization': `Bearer ${state.token}` } });
    if (!res.ok) throw new Error(t('toast_pdf_com_err'));
    const blob = await res.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `comisiones_tramite_${new Date().toISOString().slice(0,10)}.pdf`;
    a.click();
    toast(t('toast_pdf_ok'), 'success');
  } catch (err) { toast(err.message, 'error'); }
  finally {
    btn.disabled = false; btnArrow.disabled = false;
    btn.innerHTML = t('btn_pdf');
  }
}

// ── PDF Seguimiento ───────────────────────────────────────────

async function descargarPDFSeguimiento(tipo) {
  const btn      = g('btn-pdf-seguimiento');
  const btnArrow = g('btn-pdf-seguimiento-toggle');
  btn.disabled = true; btnArrow.disabled = true;
  btn.innerHTML = t('pdf_generating');

  const params = new URLSearchParams({ tipo, anio: state.segAnio, lang: state.lang });

  try {
    const res = await fetch(`/mayor-a-casa/seguimientos/informe/pdf?${params}`,
      { headers: { 'Authorization': `Bearer ${state.token}` } });
    if (!res.ok) throw new Error(t('toast_pdf_seg_err'));
    const blob = await res.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `seguimiento_${tipo}_${state.segAnio}.pdf`;
    a.click();
    toast(t('toast_pdf_ok'), 'success');
  } catch (err) { toast(err.message, 'error'); }
  finally {
    btn.disabled = false; btnArrow.disabled = false;
    btn.innerHTML = t('btn_pdf');
  }
}

// ── Toast ─────────────────────────────────────────────────────

function toast(msg, type = 'info') {
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.innerHTML = `<span class="toast-icon">${icons[type] || 'ℹ'}</span><span>${msg}</span>`;
  g('toast-container').appendChild(el);
  requestAnimationFrame(() => el.classList.add('show'));
  setTimeout(() => { el.classList.remove('show'); setTimeout(() => el.remove(), 300); }, 3500);
}

// ── Inicialización ────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  applyI18n();
  initApp();

  // Auth
  g('login-form').addEventListener('submit', onLoginSubmit);
  g('btn-logout').addEventListener('click', logout);
  g('btn-theme').addEventListener('click', toggleTheme);
  g('btn-lang').addEventListener('click', toggleLang);

  g('toggle-pwd').addEventListener('click', () => {
    const input = g('login-pass');
    const isPass = input.type === 'password';
    input.type = isPass ? 'text' : 'password';
    g('pwd-eye').textContent = isPass ? '🙈' : '👁';
  });

  // Inner tabs
  g('inner-tabs-nav').addEventListener('click', e => {
    const btn = e.target.closest('.inner-tab');
    if (btn && btn.dataset.itab) switchInnerTab(btn.dataset.itab);
  });

  // PDF
  g('btn-pdf').addEventListener('click', () => descargarPDF('activos'));
  g('btn-pdf-toggle').addEventListener('click', e => {
    e.stopPropagation();
    g('pdf-menu').classList.toggle('hidden');
  });
  g('pdf-menu').addEventListener('click', e => {
    const item = e.target.closest('.split-menu-item');
    if (!item) return;
    g('pdf-menu').classList.add('hidden');
    descargarPDF(item.dataset.tipo);
  });
  document.addEventListener('click', () => {
    ['pdf-menu','pdf-menu-facturas','pdf-menu-comisiones','pdf-menu-seguimiento'].forEach(id => {
      const m = g(id); if (m) m.classList.add('hidden');
    });
  });

  // Nuevo caso (Usuarios ya no tiene este botón — está en Comisiones)
  g('btn-nuevo-comision').addEventListener('click', () => {
    switchInnerTab('comisiones');
    abrirModal(null, 'comision');
  });

  // Modal
  g('caso-form').addEventListener('submit', onFormSubmit);
  g('modal-close').addEventListener('click', cerrarModal);
  g('modal-cancel').addEventListener('click', cerrarModal);
  g('modal-backdrop').addEventListener('click', e => {
    if (e.target === g('modal-backdrop')) cerrarModal();
  });
  g('f-activo').addEventListener('change', () => {
    updateToggleLabel();
    if (!g('f-activo').checked) g('f-baja').value  = new Date().toISOString().slice(0,10);
    else                         g('f-baja').value  = '';
  });
  g('btn-eliminar').addEventListener('click', () => {
    if (state.modalMode === 'comision') {
      const com = state.comisiones.find(c => c.id === state.editingComisionId);
      if (com && confirm(`${t('confirm_del')} ${com.apellidos}?`)) {
        eliminarComision(com.id).then(() => { cerrarModal(); toast(t('toast_deleted'), 'info'); }).catch(err => toast(err.message,'error'));
      }
    } else {
      const caso = state.casos.find(c => c.id === state.editingId);
      if (caso) confirmarEliminarCaso(caso);
    }
  });
  g('btn-aprobar').addEventListener('click', () => {
    const com = state.comisiones.find(c => c.id === state.editingComisionId);
    if (!com) return;
    if (confirm(`${t('confirm_aprobar')} ${com.apellidos}?`)) {
      aprobarComision(com.id).catch(err => toast(err.message, 'error'));
    }
  });

  // Zona filters (Usuarios)
  g('zona-filters').addEventListener('click', e => {
    const btn = e.target.closest('.filter-btn');
    if (!btn) return;
    document.querySelectorAll('#zona-filters .filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.filterZona = btn.dataset.zona === '' ? null : parseInt(btn.dataset.zona);
    renderTabla();
    renderStats();
    renderStats();
  });

  // Zona filters (Comisiones)
  g('zona-filters-comision').addEventListener('click', e => {
    const btn = e.target.closest('.filter-btn');
    if (!btn) return;
    document.querySelectorAll('#zona-filters-comision .filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.filterComisionZona = btn.dataset.zonaC === '' ? null : parseInt(btn.dataset.zonaC);
    renderComisiones();
    renderStatsComisiones();
    renderStatsComisiones();
  });

  // SIP search (Usuarios)
  g('sip-search').addEventListener('input', e => {
    state.sipSearch = e.target.value.trim();
    renderTabla();
  });

  // SIP search (Comisiones)
  g('sip-search-comision').addEventListener('input', e => {
    state.sipSearchComision = e.target.value.trim();
    renderComisiones();
    renderStatsComisiones();
  });

  // Mes filter (Comisiones)
  g('com-mes-filter').addEventListener('change', e => {
    state.filterComisionMes = e.target.value || null;
    renderComisiones();
    renderStatsComisiones();
    renderStatsComisiones();
  });

  // Sort buttons
  document.querySelectorAll('.sort-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const key = btn.dataset.sort;
      if (state.sortBy === key) state.sortDir = state.sortDir === 'asc' ? 'desc' : 'asc';
      else {
        state.sortBy  = key;
        state.sortDir = (key === 'fecha_alta' || key === 'renovacion') ? 'desc' : 'asc';
      }
      updateSortUI();
      renderTabla();
    });
  });

  // PDF Facturas
  g('btn-pdf-facturas').addEventListener('click', () => descargarPDFFacturas());
  g('btn-pdf-facturas-toggle').addEventListener('click', e => {
    e.stopPropagation();
    g('pdf-menu-facturas').classList.toggle('hidden');
  });
  g('pdf-menu-facturas').addEventListener('click', e => {
    const item = e.target.closest('.split-menu-item');
    if (!item) return;
    g('pdf-menu-facturas').classList.add('hidden');
    descargarPDFFacturas();
  });

  // PDF Comisiones
  g('btn-pdf-comisiones').addEventListener('click', () => descargarPDFComisiones());
  g('btn-pdf-comisiones-toggle').addEventListener('click', e => {
    e.stopPropagation();
    g('pdf-menu-comisiones').classList.toggle('hidden');
  });
  g('pdf-menu-comisiones').addEventListener('click', e => {
    const item = e.target.closest('.split-menu-item');
    if (!item) return;
    g('pdf-menu-comisiones').classList.add('hidden');
    descargarPDFComisiones();
  });

  // PDF Seguimiento
  g('btn-pdf-seguimiento').addEventListener('click', () => descargarPDFSeguimiento(state.segTab));
  g('btn-pdf-seguimiento-toggle').addEventListener('click', e => {
    e.stopPropagation();
    g('pdf-menu-seguimiento').classList.toggle('hidden');
  });
  g('pdf-menu-seguimiento').addEventListener('click', e => {
    const item = e.target.closest('.split-menu-item');
    if (!item) return;
    g('pdf-menu-seguimiento').classList.add('hidden');
    descargarPDFSeguimiento(item.dataset.tipo);
  });

  // Seguimiento sub-tabs
  const segTabsNav = g('seg-tabs-nav');
  if (segTabsNav) {
    segTabsNav.addEventListener('click', e => {
      const btn = e.target.closest('.inner-tab');
      if (!btn || !btn.dataset.segtab) return;
      const tipo = btn.dataset.segtab;
      state.segTab = tipo;
      segTabsNav.querySelectorAll('.inner-tab').forEach(b => b.classList.toggle('active', b.dataset.segtab === tipo));
      document.querySelectorAll('.seg-tab-panel').forEach(p => p.classList.toggle('hidden', p.id !== `segtab-${tipo}`));
    });
  }

  // Nuevo documento modal
  g('btn-nuevo-doc').addEventListener('click', () => {
    state.editingDocId = null;
    g('f-doc-titulo').value = '';
    g('doc-btn-eliminar').classList.add('hidden');
    g('doc-modal-backdrop').classList.remove('hidden');
  });
  g('doc-modal-close').addEventListener('click', () => g('doc-modal-backdrop').classList.add('hidden'));
  g('doc-modal-cancel').addEventListener('click', () => g('doc-modal-backdrop').classList.add('hidden'));
  g('doc-modal-backdrop').addEventListener('click', e => {
    if (e.target === g('doc-modal-backdrop')) g('doc-modal-backdrop').classList.add('hidden');
  });
  g('doc-form').addEventListener('submit', async e => {
    e.preventDefault();
    const titulo = g('f-doc-titulo').value.trim();
    if (!titulo) { toast(t('val_required'), 'error'); return; }
    g('doc-modal-submit').disabled = true;
    try {
      if (state.editingDocId) {
        await actualizarDoc(state.editingDocId, { titulo });
      } else {
        await crearDoc(titulo);
      }
      g('doc-modal-backdrop').classList.add('hidden');
      toast(t('toast_doc_saved'), 'success');
    } catch (err) { toast(err.message, 'error'); }
    finally { g('doc-modal-submit').disabled = false; }
  });
  g('doc-btn-eliminar').addEventListener('click', async () => {
    if (!state.editingDocId) return;
    const doc = state.docs.find(d => d.id === state.editingDocId);
    if (doc && confirm(`${t('confirm_del_doc')} "${doc.titulo}"?`)) {
      try {
        await eliminarDoc(state.editingDocId);
        g('doc-modal-backdrop').classList.add('hidden');
        toast(t('toast_doc_deleted'), 'info');
      } catch (err) { toast(err.message, 'error'); }
    }
  });
});
