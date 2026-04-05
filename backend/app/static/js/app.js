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
    view_title:    'Major a Casa',
    stat_total:    'Total casos',
    stat_activos:  'Activos',
    stat_bajas:    'Dados de baja',
    stat_zonas:    'Zonas con casos',
    stat_hombres:  'Hombres',
    stat_mujeres:  'Mujeres',
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
    th_sexo:       'Sexo',
    th_telefono:   'Teléfono',
    th_renov:      'Mes Renov.',
    th_alta:       'Fecha Alta',
    th_estado:     'Estado',
    th_acciones:   'Acciones',
    loading:       'Cargando casos…',
    btn_pdf:       '<span>📊</span> Generar Informe PDF',
    pdf_activos:   '📋 Todos los casos activos',
    pdf_renov:     '📅 Renovación del mes actual',
    itab_usuarios:  '👥 Usuarios',
    itab_facturas:  '📄 Facturas',
    itab_comisiones: '📋 Comisiones',
    th_mes:        'Mes',
    th_anio:       'Año',
    th_cuantia:    'Cuantía',
    th_fecha:      'Fecha',
    th_num_exp:    'Expediente',
    empty_facturas: 'No hay facturas registradas',
    empty_comisiones: 'No hay comisiones registradas',
    btn_nuevo:     '<span>✦</span> Nuevo caso',
    lbl_apellidos: 'Apellidos <span class="req">*</span>',
    lbl_nombre:    'Nombre <span class="req">*</span>',
    lbl_dni:       'DNI',
    lbl_sip:       'SIP <span class="field-hint-inline">(8 dígitos)</span>',
    hint_dni:      '8 dígitos + 1 letra',
    hint_sip_inline: '(8 dígitos)',
    lbl_zona_field:'Zona',
    lbl_sexo:      'Sexo',
    lbl_telefono:  'Teléfono',
    lbl_renov:     'Mes de renovación',
    lbl_alta:      'Fecha de alta',
    lbl_baja:      'Fecha de baja',
    lbl_direccion: 'Dirección',
    lbl_estado:    'Estado del caso',
    lbl_obs:       'Observaciones / Notas',
    btn_eliminar:  '🗑️ Eliminar caso',
    btn_cancelar:  'Cancelar',
    btn_guardar:   'Guardar',
    modal_new:     'Nuevo Caso',
    modal_edit:    'Editar Caso',
    modal_sub_new: 'Rellena los datos',
    sex_hombre:    'Hombre',
    sex_mujer:     'Mujer',
    sex_no_define: 'No define',
    badge_activo:  '● Activo',
    badge_baja:    '○ Baja',
    empty_no_data: 'No hay casos registrados.',
    empty_no_filter:'Sin resultados para el filtro aplicado.',
    toggle_activo: 'Activo',
    toggle_baja:   'Dado de baja',
    toast_saved:   'Guardado correctamente',
    toast_deleted: 'Eliminado',
    toast_load_err:'Error al cargar datos',
    toast_pdf_ok:  'PDF descargado',
    toast_pdf_err: 'Error al generar PDF',
    confirm_del:   '¿Eliminar caso de',
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
  },
  val: {
    login_sub:     'Accés per a APB — Regidoria de Benestar Social',
    login_footer:  'La sessió dura 8 hores · Token xifrat JWT',
    lbl_usuario:   'Usuari del departament',
    lbl_password:  'Contrasenya',
    btn_login:     'Iniciar sessió',
    btn_logout:    'Tancar sessió',
    view_title:    'Major a Casa',
    stat_total:    'Total casos',
    stat_activos:  'Actius',
    stat_bajas:    'Donats de baixa',
    stat_zonas:    'Zones amb casos',
    stat_hombres:  'Homes',
    stat_mujeres:  'Dones',
    lbl_zona:      'Zona:',
    zona_todas:    'Totes',
    lbl_ordenar:   'Ordenar:',
    sort_nombre:   'Nom',
    sort_renov:    'Renovació',
    sort_alta:     'Alta',
    sort_estado:   'Estat',
    sip_search_placeholder: 'Buscar per SIP…',
    th_nombre:     'Cognoms, Nom',
    th_zona:       'Zona',
    th_sexo:       'Sexe',
    th_telefono:   'Telèfon',
    th_renov:      'Mes Renov.',
    th_alta:       "Data d'Alta",
    th_estado:     'Estat',
    th_acciones:   'Accions',
    loading:       'Carregant casos…',
    btn_pdf:       '<span>📊</span> Generar Informe PDF',
    pdf_activos:   '📋 Tots els casos actius',
    pdf_renov:     '📅 Renovació del mes actual',
    itab_usuarios:  '👥 Usuaris',
    itab_facturas:  '📄 Factures',
    itab_comisiones: '📋 Comissions',
    th_mes:        'Mes',
    th_anio:       'Any',
    th_cuantia:    'Quantia',
    th_fecha:      'Data',
    th_num_exp:    'Expedient',
    empty_facturas: 'No hi ha factures registrades',
    empty_comisiones: 'No hi ha comissions registrades',
    btn_nuevo:     '<span>✦</span> Nou cas',
    lbl_apellidos: 'Cognoms <span class="req">*</span>',
    lbl_nombre:    'Nom <span class="req">*</span>',
    lbl_dni:       'DNI',
    lbl_sip:       'SIP <span class="field-hint-inline">(8 dígits)</span>',
    hint_dni:      '8 dígits + 1 lletra',
    hint_sip_inline: '(8 dígits)',
    lbl_zona_field:'Zona',
    lbl_sexo:      'Sexe',
    lbl_telefono:  'Telèfon',
    lbl_renov:     'Mes de renovació',
    lbl_alta:      "Data d'alta",
    lbl_baja:      'Data de baixa',
    lbl_direccion: 'Adreça',
    lbl_estado:    'Estat del cas',
    lbl_obs:       'Observacions / Notes',
    btn_eliminar:  '🗑️ Eliminar cas',
    btn_cancelar:  'Cancel·lar',
    btn_guardar:   'Guardar',
    modal_new:     'Nou Cas',
    modal_edit:    'Editar Cas',
    modal_sub_new: 'Emplena les dades',
    sex_hombre:    'Home',
    sex_mujer:     'Dona',
    sex_no_define: 'No es definix',
    badge_activo:  '● Actiu',
    badge_baja:    '○ Baixa',
    empty_no_data: 'No hi ha casos registrats.',
    empty_no_filter:'Sense resultats per al filtre aplicat.',
    toggle_activo: 'Actiu',
    toggle_baja:   'Donat de baixa',
    toast_saved:   'Guardat correctament',
    toast_deleted: 'Eliminat',
    toast_load_err:'Error en carregar dades',
    toast_pdf_ok:  'PDF descarregat',
    toast_pdf_err: 'Error en generar PDF',
    confirm_del:   'Eliminar cas de',
    login_empty:   'Introdueix usuari i contrasenya',
    login_verify:  'Verificant...',
    pdf_generating:'<span>⏳</span> Generant...',
    val_required:  'Camps obligatoris que falten',
    val_dni_or_sip:'Has d\'introduir almenys DNI o SIP',
    val_dni_bad:   'El DNI ha de tindre 8 dígits i 1 lletra (ex: 12345678X)',
    val_sip_bad:   'El SIP ha de tindre exactament 8 dígits',
    welcome:       'Benvingut,',
    opt_no_asignar:'— Sense assignar —',
    opt_no_sexo:   '— No especificat —',
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
  // Update sort buttons — keep arrow icons
  document.querySelectorAll('.sort-btn').forEach(btn => {
    const key = btn.getAttribute('data-i18n');
    const dirEl = btn.querySelector('.sort-dir');
    if (key && dirEl) {
      const dirHTML = dirEl.outerHTML;
      btn.innerHTML = t(key) + ' ' + dirHTML;
    }
  });
  // Update lang button label
  const langBtn = g('btn-lang');
  if (langBtn) langBtn.textContent = state.lang === 'es' ? 'ES' : 'VAL';
}

// ── Estado global de la app ───────────────────────────────────
const state = {
  casos: [],
  editingId: null,
  token: localStorage.getItem('apbapp_token'),
  deptName: localStorage.getItem('apbapp_dept'),
  sortBy:  'nombre',
  sortDir: 'asc',
  filterZona: null,
  sipSearch: '',
  lang: localStorage.getItem('apbapp_lang') || 'es',
  innerTab: 'usuarios',
};

// ── Utilidades ────────────────────────────────────────────────

function g(id) { return document.getElementById(id); }

function switchInnerTab(tabName) {
  state.innerTab = tabName;
  document.querySelectorAll('.inner-tab').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.itab === tabName);
  });
  document.querySelectorAll('.inner-tab-panel').forEach(panel => {
    panel.classList.toggle('hidden', panel.id !== `itab-${tabName}`);
  });
  // Load specialized data if needed
  if (tabName === 'usuarios') cargarCasos();
  else if (tabName === 'facturas') cargarFacturas();
  else if (tabName === 'comisiones') cargarComisiones();
}

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

function highlightMatch(text, query) {
  if (!query || !text) return esc(text);
  const escapedText = esc(text);
  const escapedQuery = esc(query);
  const regex = new RegExp(`(${escapedQuery})`, 'gi');
  return escapedText.replace(regex, '<span class="sip-highlight">$1</span>');
}

// ── Validación DNI / SIP ─────────────────────────────────────

const RE_DNI = /^\d{8}[A-Za-z]$/;
const RE_SIP = /^\d{8}$/;

function validarDniSip(dni, sip) {
  let errors = [];
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
  const btn = g('login-btn');

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
    state.token = data.access_token;
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
  cargarCasos().catch(err => {
    if (err.message.includes('Sesión')) return;
    toast(t('toast_load_err'), 'error');
  });
}

// ── API: CRUD ─────────────────────────────────────────────────

async function cargarCasos() {
  state.casos = await api('GET', '/mayor-a-casa/casos/');
  renderTabla();
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

// ── Estadísticas (relativas a zona) ──────────────────────────

function renderStats() {
  // Use filtered list (by zone) for stats
  let list = [...state.casos];
  if (state.filterZona !== null) {
    list = list.filter(c => c.zona === state.filterZona);
  }

  const total   = list.length;
  const activos = list.filter(c => c.activo).length;
  const bajas   = total - activos;
  const zonas   = new Set(list.map(c => c.zona).filter(Boolean)).size;
  const hombres = list.filter(c => c.sexo === 'hombre').length;
  const mujeres = list.filter(c => c.sexo === 'mujer').length;

  g('stat-total').textContent   = total;
  g('stat-activos').textContent = activos;
  g('stat-bajas').textContent   = bajas;
  g('stat-zonas').textContent   = zonas;
  g('stat-hombres').textContent = hombres;
  g('stat-mujeres').textContent = mujeres;
}

// ── Filtrado y ordenación ─────────────────────────────────────

function getFilteredSorted() {
  let list = [...state.casos];

  if (state.filterZona !== null) {
    list = list.filter(c => c.zona === state.filterZona);
  }

  // SIP search filter (case-insensitive)
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
      if (!a.fecha_alta) return 1;
      if (!b.fecha_alta) return -1;
      va = a.fecha_alta; vb = b.fecha_alta;
    } else if (state.sortBy === 'renovacion') {
      if (!a.mes_renovacion && !b.mes_renovacion) return 0;
      if (!a.mes_renovacion) return 1;
      if (!b.mes_renovacion) return -1;
      va = a.mes_renovacion; vb = b.mes_renovacion;
    } else if (state.sortBy === 'activo') {
      va = a.activo ? 0 : 1;
      vb = b.activo ? 0 : 1;
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
    if (dirEl) {
      dirEl.textContent = !isActive ? '↕' : (state.sortDir === 'asc' ? '↑' : '↓');
    }
  });
}

// ── Tabla ─────────────────────────────────────────────────────

function renderTabla() {
  const tbody = g('tbody-casos');
  const list  = getFilteredSorted();

  const countEl = g('results-count');
  if (countEl) {
    const total = state.casos.length;
    countEl.textContent = list.length === total
      ? `${total} caso${total !== 1 ? 's' : ''}`
      : `${list.length} de ${total}`;
  }

  const sexLabels = {
    hombre: t('sex_hombre'), mujer: t('sex_mujer'), no_define: t('sex_no_define'),
  };

  if (!state.casos.length) {
    tbody.innerHTML = `<tr><td colspan="10" class="empty-cell">${t('empty_no_data')}</td></tr>`;
    return;
  }
  if (!list.length) {
    tbody.innerHTML = `<tr><td colspan="10" class="empty-cell">${t('empty_no_filter')}</td></tr>`;
    return;
  }

  tbody.innerHTML = list.map(c => `
    <tr data-id="${c.id}">
      <td class="td-name"><strong>${esc(c.apellidos)}</strong>,&nbsp;${esc(c.nombre)}</td>
      <td>${esc(c.dni) || '—'}</td>
      <td>${highlightMatch(c.sip, state.sipSearch) || '—'}</td>
      <td>${c.zona ? `<span class="zona-badge" data-zona="${c.zona}">Zona ${c.zona}</span>` : '—'}</td>
      <td>${sexLabels[c.sexo] || '—'}</td>
      <td>${esc(c.telefono) || '—'}</td>
      <td>${formatMes(c.mes_renovacion)}</td>
      <td>${formatFecha(c.fecha_alta)}</td>
      <td><span class="badge ${c.activo ? 'badge-activo' : 'badge-baja'}">${c.activo ? t('badge_activo') : t('badge_baja')}</span></td>
      <td class="td-actions">
        <button class="btn-icon edit-btn" data-id="${c.id}">✏️</button>
        <button class="btn-icon delete-btn" data-id="${c.id}">🗑</button>
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
      pedirConfirmacionEliminar(state.casos.find(c => c.id === parseInt(btn.dataset.id)));
    });
  });
}

// ── Tema claro/oscuro ─────────────────────────────────────────

function initTheme() {
  const saved = localStorage.getItem('apbapp_theme') || 'dark';
  applyTheme(saved);
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('apbapp_theme', theme);
  const btn = g('btn-theme');
  if (btn) btn.textContent = theme === 'dark' ? '🌙' : '☀️';
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  applyTheme(current === 'dark' ? 'light' : 'dark');
}

// ── Idioma ────────────────────────────────────────────────────

function toggleLang() {
  state.lang = state.lang === 'es' ? 'val' : 'es';
  localStorage.setItem('apbapp_lang', state.lang);
  applyI18n();
  // Refresh entire UI
  renderTabla();
  renderStats();
  if (state.editingId) {
    const caso = state.casos.find(c => c.id === state.editingId);
    if (caso) abrirModal(caso);
  } else if (!g('modal-backdrop').classList.contains('hidden')) {
    abrirModal();
  }
}

// ── Modal ─────────────────────────────────────────────────────

function abrirModal(caso = null) {
  state.editingId = caso ? caso.id : null;
  g('modal-title').textContent = caso ? t('modal_edit') : t('modal_new');
  g('modal-subtitle').textContent = caso ? `${caso.apellidos}, ${caso.nombre}` : t('modal_sub_new');
  g('btn-eliminar').classList.toggle('hidden', !caso);
  g('caso-form').reset();

  // Clear validation hints
  const dniHint = g('dni-hint');
  if (dniHint) { dniHint.textContent = t('hint_dni'); dniHint.classList.remove('error'); }

  if (caso) {
    g('f-apellidos').value = caso.apellidos || '';
    g('f-nombre').value = caso.nombre || '';
    g('f-dni').value = caso.dni || '';
    g('f-sip').value = caso.sip || '';
    g('f-zona').value = caso.zona || '';
    g('f-sexo').value = caso.sexo || '';
    g('f-tel').value = caso.telefono || '';
    g('f-renov').value = caso.mes_renovacion || '';
    g('f-alta').value = caso.fecha_alta || '';
    g('f-baja').value = caso.fecha_baja || '';
    g('f-dir').value = caso.direccion || '';
    g('f-activo').checked = caso.activo !== false;
    g('f-obs').value = caso.observaciones || '';
    updateToggleLabel();
  } else {
    g('f-renov').value = new Date().toISOString().slice(0, 7);
    g('f-alta').value = new Date().toISOString().slice(0, 10);
  }

  g('modal-backdrop').classList.remove('hidden');
  g('modal-submit').disabled = false;
  g('modal-submit').textContent = t('btn_guardar');
}

function cerrarModal() { g('modal-backdrop').classList.add('hidden'); state.editingId = null; }

function updateToggleLabel() {
  const checked = g('f-activo').checked;
  g('toggle-label-text').textContent = checked ? t('toggle_activo') : t('toggle_baja');
  g('toggle-label-text').style.color = checked ? 'var(--success)' : 'var(--text-3)';
}

async function onFormSubmit(e) {
  e.preventDefault();
  const dni = g('f-dni').value.trim();
  const sip = g('f-sip').value.trim();
  const apellidos = g('f-apellidos').value.trim();
  const nombre = g('f-nombre').value.trim();

  const valErrors = validarDniSip(dni, sip);
  
  // Clean previous errors
  ['f-apellidos','f-nombre','f-dni','f-sip'].forEach(id => g(id).classList.remove('input-error'));

  if (!apellidos || !nombre) {
    if (!apellidos) g('f-apellidos').classList.add('input-error');
    if (!nombre) g('f-nombre').classList.add('input-error');
    toast(t('val_required'), 'error');
    return;
  }

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

  const datos = {
    apellidos,
    nombre,
    dni: dni || null,
    sip: sip || null,
    zona: g('f-zona').value ? parseInt(g('f-zona').value) : null,
    sexo: g('f-sexo').value || null,
    mes_renovacion: g('f-renov').value || null,
    telefono: g('f-tel').value.trim() || null,
    fecha_alta: g('f-alta').value || null,
    fecha_baja: g('f-baja').value || null,
    direccion: g('f-dir').value.trim() || null,
    activo: g('f-activo').checked,
    observaciones: g('f-obs').value.trim() || null,
  };

  try {
    if (state.editingId) await actualizarCaso(state.editingId, datos);
    else await crearCaso(datos);
    cerrarModal();
    toast(t('toast_saved'), 'success');
  } catch (err) { toast(err.message, 'error'); }
}

function pedirConfirmacionEliminar(caso) {
  if (confirm(`${t('confirm_del')} ${caso.apellidos}?`)) {
    eliminarCaso(caso.id).then(() => toast(t('toast_deleted'), 'info')).catch(err => toast(err.message, 'error'));
  }
}

async function descargarPDF(tipo = 'activos') {
  const btn      = g('btn-pdf');
  const btnArrow = g('btn-pdf-toggle');
  btn.disabled = true;
  btnArrow.disabled = true;
  btn.innerHTML = t('pdf_generating');

  let path = tipo === 'renovacion'
    ? '/mayor-a-casa/casos/informe/pdf/renovacion'
    : '/mayor-a-casa/casos/informe/pdf';
  
  const params = new URLSearchParams();
  if (state.filterZona) params.append('zona', state.filterZona);
  params.append('lang', state.lang);
  
  if (params.toString()) {
    path += `?${params.toString()}`;
  }

  try {
    const res = await fetch(path, {
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (!res.ok) throw new Error(t('toast_pdf_err'));
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `informe_${new Date().toISOString().slice(0, 10)}.pdf`;
    a.click();
    toast(t('toast_pdf_ok'), 'success');
  } catch (err) { toast(err.message, 'error'); }
  finally {
    btn.disabled = false;
    btnArrow.disabled = false;
    btn.innerHTML = t('btn_pdf');
  }
}

function toast(msg, type = 'info') {
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.innerHTML = `<span class="toast-icon">${icons[type]}</span><span>${msg}</span>`;
  g('toast-container').appendChild(el);
  requestAnimationFrame(() => el.classList.add('show'));
  setTimeout(() => { el.classList.remove('show'); setTimeout(() => el.remove(), 300); }, 3000);
}

// ── Inicialización ────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  applyI18n();
  initApp();

  g('login-form').addEventListener('submit', onLoginSubmit);
  g('btn-logout').addEventListener('click', logout);
  g('btn-theme').addEventListener('click', toggleTheme);
  g('btn-lang').addEventListener('click', toggleLang);

  // Inner tabs switching
  document.querySelectorAll('.inner-tab').forEach(btn => {
    btn.addEventListener('click', () => {
      switchInnerTab(btn.dataset.itab);
    });
  });

  g('toggle-pwd').addEventListener('click', () => {
    const input = g('login-pass');
    const isPass = input.type === 'password';
    input.type = isPass ? 'text' : 'password';
    g('pwd-eye').textContent = isPass ? '🙈' : '👁';
  });

  g('btn-nuevo').addEventListener('click', () => abrirModal());
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
    const menu = g('pdf-menu');
    if (menu) menu.classList.add('hidden');
  });
  g('caso-form').addEventListener('submit', onFormSubmit);
  g('modal-close').addEventListener('click', cerrarModal);
  g('modal-cancel').addEventListener('click', cerrarModal);
  g('f-activo').addEventListener('change', () => {
    updateToggleLabel();
    // Automatic discharge date logic
    if (!g('f-activo').checked) {
      g('f-baja').value = new Date().toISOString().slice(0, 10);
    } else {
      g('f-baja').value = '';
    }
  });

  g('modal-backdrop').addEventListener('click', e => {
    if (e.target === g('modal-backdrop')) cerrarModal();
  });

  g('btn-eliminar').addEventListener('click', () => {
    const caso = state.casos.find(c => c.id === state.editingId);
    if (caso) pedirConfirmacionEliminar(caso);
  });

  // Zona filters
  g('zona-filters').addEventListener('click', e => {
    const btn = e.target.closest('.filter-btn');
    if (!btn) return;
    document.querySelectorAll('#zona-filters .filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.filterZona = btn.dataset.zona === '' ? null : parseInt(btn.dataset.zona);
    renderTabla();
    renderStats();
  });

  // SIP search
  g('sip-search').addEventListener('input', e => {
    state.sipSearch = e.target.value.trim();
    renderTabla();
  });

  // Sort buttons
  document.querySelectorAll('.sort-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const key = btn.dataset.sort;
      if (state.sortBy === key) {
        state.sortDir = state.sortDir === 'asc' ? 'desc' : 'asc';
      } else {
        state.sortBy = key;
        // Default sort direction: descending for dates, ascending for text
        state.sortDir = (key === 'fecha_alta' || key === 'renovacion') ? 'desc' : 'asc';
      }
      updateSortUI();
      renderTabla();
    });
  });
});
