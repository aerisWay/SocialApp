/* ============================================================
   app.js — Lógica del frontend de SocialApp
   ============================================================ */

'use strict';

// ── Estado global de la app ───────────────────────────────────
const state = {
  casos: [],       // Lista de casos cargados desde la API
  editingId: null, // null = crear nuevo, número = editar ese ID
  token: localStorage.getItem('socialapp_token'),
  deptName: localStorage.getItem('socialapp_dept'),
  sortBy:  'nombre',   // 'nombre' | 'renovacion' | 'activo'
  sortDir: 'asc',      // 'asc' | 'desc'
  filterZona: null,    // null = todas, o 1/2/3/4
};

// ── Utilidades ────────────────────────────────────────────────

function g(id) { return document.getElementById(id); }

/** Llama a la API del backend. Incluye el token si existe. */
async function api(method, path, body = null) {
  const headers = { 'Content-Type': 'application/json' };
  if (state.token) {
    headers['Authorization'] = `Bearer ${state.token}`;
  }

  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(path, opts);

  // Si el servidor dice 401 (No autorizado), cerramos sesión automáticamente
  if (res.status === 401) {
    logout();
    throw new Error('Sesión expirada o no autorizada');
  }

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

// ── Autenticación ─────────────────────────────────────────────

async function onLoginSubmit(e) {
  e.preventDefault();
  const user = g('login-user').value.trim();
  const pass = g('login-pass').value.trim();
  const errEl = g('login-error');
  const btn = g('login-btn');

  if (!user || !pass) {
    errEl.classList.remove('hidden');
    g('login-error-msg').textContent = 'Introduce usuario y contraseña';
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Verificando...';
  errEl.classList.add('hidden');

  try {
    const data = await api('POST', '/auth/login', { username: user, password: pass });
    
    // Guardar sesión
    state.token = data.access_token;
    state.deptName = data.dept_name;
    localStorage.setItem('socialapp_token', data.access_token);
    localStorage.setItem('socialapp_dept', data.dept_name);

    // Mostrar app
    initApp();
    toast(`Bienvenido, ${state.deptName}`, 'success');
  } catch (err) {
    errEl.classList.remove('hidden');
    g('login-error-msg').textContent = err.message;
    btn.disabled = false;
    btn.textContent = 'Iniciar sesión';
  }
}

function logout() {
  state.token = null;
  state.deptName = null;
  localStorage.removeItem('socialapp_token');
  localStorage.removeItem('socialapp_dept');
  
  g('main-app').classList.add('hidden');
  g('login-screen').classList.remove('hidden');
  g('login-form').reset();
  g('login-btn').disabled = false;
  g('login-btn').textContent = 'Iniciar sesión';
}

function initApp() {
  if (!state.token) {
    g('login-screen').classList.remove('hidden');
    g('main-app').classList.add('hidden');
    return;
  }

  g('login-screen').classList.add('hidden');
  g('main-app').classList.remove('hidden');
  g('dept-name-display').textContent = state.deptName;

  cargarCasos().catch(err => {
    if (err.message.includes('Sesión')) return; // logout() ya se encargó
    toast('Error al cargar datos', 'error');
  });
}

// ── API: operaciones CRUD ─────────────────────────────────────

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

// ── Estadísticas ──────────────────────────────────────────────

function renderStats() {
  const total   = state.casos.length;
  const activos = state.casos.filter(c => c.activo).length;
  const bajas   = total - activos;
  const zonas   = new Set(state.casos.map(c => c.zona).filter(Boolean)).size;
  const hombres = state.casos.filter(c => c.sexo === 'hombre').length;
  const mujeres = state.casos.filter(c => c.sexo === 'mujer').length;

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

  list.sort((a, b) => {
    if (state.sortBy === 'nombre') {
      const sa = `${a.apellidos || ''} ${a.nombre || ''}`;
      const sb = `${b.apellidos || ''} ${b.nombre || ''}`;
      const cmp = sa.localeCompare(sb, 'es', { sensitivity: 'base' });
      return state.sortDir === 'asc' ? cmp : -cmp;
    }
    let va, vb;
    if (state.sortBy === 'renovacion') {
      // Nulos al final siempre
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
      if (!isActive) { dirEl.textContent = '↕'; }
      else { dirEl.textContent = state.sortDir === 'asc' ? '↑' : '↓'; }
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

  if (!state.casos.length) {
    tbody.innerHTML = `<tr><td colspan="9" class="empty-cell">No hay casos registrados.</td></tr>`;
    return;
  }
  if (!list.length) {
    tbody.innerHTML = `<tr><td colspan="9" class="empty-cell">Sin resultados para el filtro aplicado.</td></tr>`;
    return;
  }

  tbody.innerHTML = list.map(c => `
    <tr data-id="${c.id}">
      <td class="td-name"><strong>${esc(c.apellidos)}</strong>,&nbsp;${esc(c.nombre)}</td>
      <td>${esc(c.dni_sip)}</td>
      <td>${c.zona ? `<span class="zona-badge" data-zona="${c.zona}">Zona ${c.zona}</span>` : '—'}</td>
      <td>${({hombre:'Hombre',mujer:'Mujer',no_define:'No define'})[c.sexo] || '—'}</td>
      <td>${esc(c.telefono) || '—'}</td>
      <td>${formatMes(c.mes_renovacion)}</td>
      <td>${formatFecha(c.fecha_alta)}</td>
      <td><span class="badge ${c.activo ? 'badge-activo' : 'badge-baja'}">${c.activo ? '● Activo' : '○ Baja'}</span></td>
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
  const saved = localStorage.getItem('socialapp_theme') || 'dark';
  applyTheme(saved);
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('socialapp_theme', theme);
  const btn = g('btn-theme');
  if (btn) btn.textContent = theme === 'dark' ? '🌙' : '☀️';
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  applyTheme(current === 'dark' ? 'light' : 'dark');
}

// ── Modal ─────────────────────────────────────────────────────

function abrirModal(caso = null) {
  state.editingId = caso ? caso.id : null;
  g('modal-title').textContent = caso ? 'Editar Caso' : 'Nuevo Caso';
  g('modal-subtitle').textContent = caso ? `${caso.apellidos}, ${caso.nombre}` : 'Rellena los datos';
  g('btn-eliminar').classList.toggle('hidden', !caso);
  g('caso-form').reset();

  if (caso) {
    g('f-apellidos').value = caso.apellidos || '';
    g('f-nombre').value = caso.nombre || '';
    g('f-dni').value = caso.dni_sip || '';
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
  }

  g('modal-backdrop').classList.remove('hidden');
  g('modal-submit').disabled = false;
  g('modal-submit').textContent = 'Guardar';
}

function cerrarModal() { g('modal-backdrop').classList.add('hidden'); state.editingId = null; }

function updateToggleLabel() {
  const checked = g('f-activo').checked;
  g('toggle-label-text').textContent = checked ? 'Activo' : 'Dado de baja';
  g('toggle-label-text').style.color = checked ? 'var(--success)' : 'var(--text-3)';
}

async function onFormSubmit(e) {
  e.preventDefault();
  const datos = {
    apellidos: g('f-apellidos').value.trim(),
    nombre: g('f-nombre').value.trim(),
    dni_sip: g('f-dni').value.trim(),
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

  if (!datos.apellidos || !datos.nombre || !datos.dni_sip) {
    toast('Campos obligatorios faltantes', 'error');
    return;
  }

  try {
    if (state.editingId) await actualizarCaso(state.editingId, datos);
    else await crearCaso(datos);
    cerrarModal();
    toast('Guardado correctamente', 'success');
  } catch (err) { toast(err.message, 'error'); }
}

function pedirConfirmacionEliminar(caso) {
  if (confirm(`¿Eliminar caso de ${caso.apellidos}?`)) {
    eliminarCaso(caso.id).then(() => toast('Eliminado', 'info')).catch(err => toast(err.message, 'error'));
  }
}

async function descargarPDF(tipo = 'activos') {
  const btn      = g('btn-pdf');
  const btnArrow = g('btn-pdf-toggle');
  btn.disabled = true;
  btnArrow.disabled = true;
  btn.innerHTML = '<span>⏳</span> Generando...';

  const path = tipo === 'renovacion'
    ? '/mayor-a-casa/casos/informe/pdf/renovacion'
    : '/mayor-a-casa/casos/informe/pdf';

  try {
    const res = await fetch(path, {
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (!res.ok) throw new Error('Error al generar PDF');
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `informe_${new Date().toISOString().slice(0, 10)}.pdf`;
    a.click();
    toast('PDF descargado', 'success');
  } catch (err) { toast(err.message, 'error'); }
  finally {
    btn.disabled = false;
    btnArrow.disabled = false;
    btn.innerHTML = '<span>📊</span> Generar Informe PDF';
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
  initApp();

  g('login-form').addEventListener('submit', onLoginSubmit);
  g('btn-logout').addEventListener('click', logout);
  g('btn-theme').addEventListener('click', toggleTheme);

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
  g('f-activo').addEventListener('change', updateToggleLabel);

  g('modal-backdrop').addEventListener('click', e => {
    if (e.target === g('modal-backdrop')) cerrarModal();
  });

  g('btn-eliminar').addEventListener('click', () => {
    const caso = state.casos.find(c => c.id === state.editingId);
    if (caso) pedirConfirmacionEliminar(caso);
  });

  // Filtros de zona
  g('zona-filters').addEventListener('click', e => {
    const btn = e.target.closest('.filter-btn');
    if (!btn) return;
    document.querySelectorAll('#zona-filters .filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.filterZona = btn.dataset.zona === '' ? null : parseInt(btn.dataset.zona);
    renderTabla();
  });

  // Botones de ordenación
  document.querySelectorAll('.sort-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const key = btn.dataset.sort;
      if (state.sortBy === key) {
        state.sortDir = state.sortDir === 'asc' ? 'desc' : 'asc';
      } else {
        state.sortBy = key;
        state.sortDir = 'asc';
      }
      updateSortUI();
      renderTabla();
    });
  });
});
