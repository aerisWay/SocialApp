/* ============================================================
   app.js — Lógica del frontend de SocialApp
   Habla con el backend FastAPI a través de fetch (HTTP)
   ============================================================ */

'use strict';

// ── Estado global de la app ───────────────────────────────────
const state = {
  casos: [],       // Lista de casos cargados desde la API
  editingId: null, // null = crear nuevo, número = editar ese ID
};

// ── Utilidades ────────────────────────────────────────────────

/** Llama a la API del backend. Devuelve el JSON o lanza un error legible. */
async function api(method, path, body = null) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(path, opts);
  if (res.status === 204) return null; // 204 = borrado OK, sin cuerpo
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || `Error ${res.status}`);
  return data;
}

/** Convierte "2025-04" → "Abr 2025", o "—" si no hay valor */
function formatMes(val) {
  if (!val) return '—';
  const [year, month] = val.split('-').map(Number);
  const meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
  return `${meses[month - 1]} ${year}`;
}

/** Convierte "2025-04-01" → "01/04/2025", o "—" si no hay valor */
function formatFecha(val) {
  if (!val) return '—';
  const [y, m, d] = val.split('-');
  return `${d}/${m}/${y}`;
}

/** Escapa caracteres peligrosos en HTML (para evitar inyección) */
function esc(str) {
  if (!str) return '';
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
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

  document.getElementById('stat-total').textContent   = total;
  document.getElementById('stat-activos').textContent = activos;
  document.getElementById('stat-bajas').textContent   = bajas;
  document.getElementById('stat-zonas').textContent   = zonas;
}

// ── Tabla ─────────────────────────────────────────────────────

function renderTabla() {
  const tbody = document.getElementById('tbody-casos');

  if (!state.casos.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="8" class="empty-cell">
          No hay casos registrados. Haz clic en <strong>+ Nuevo caso</strong> para añadir el primero.
        </td>
      </tr>`;
    return;
  }

  tbody.innerHTML = state.casos.map(c => `
    <tr data-id="${c.id}">
      <td class="td-name"><strong>${esc(c.apellidos)}</strong>,&nbsp;${esc(c.nombre)}</td>
      <td>${esc(c.dni_sip)}</td>
      <td>${c.zona ? `<span class="zona-badge">Zona ${c.zona}</span>` : '<span style="color:var(--text-3)">—</span>'}</td>
      <td>${esc(c.telefono) || '—'}</td>
      <td>${formatMes(c.mes_renovacion)}</td>
      <td>${formatFecha(c.fecha_alta)}</td>
      <td>
        <span class="badge ${c.activo ? 'badge-activo' : 'badge-baja'}">
          ${c.activo ? '● Activo' : '○ Baja'}
        </span>
      </td>
      <td class="td-actions">
        <button class="btn-icon edit-btn"   data-id="${c.id}" title="Editar">✏️</button>
        <button class="btn-icon delete-btn" data-id="${c.id}" title="Eliminar">🗑</button>
      </td>
    </tr>
  `).join('');

  // Fila completa → abre el modal de edición
  tbody.querySelectorAll('tr[data-id]').forEach(row => {
    row.addEventListener('click', () => {
      const caso = state.casos.find(c => c.id === parseInt(row.dataset.id));
      abrirModal(caso);
    });
  });

  // Botón editar (detiene propagación para no disparar doble)
  tbody.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const caso = state.casos.find(c => c.id === parseInt(btn.dataset.id));
      abrirModal(caso);
    });
  });

  // Botón eliminar
  tbody.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async e => {
      e.stopPropagation();
      const caso = state.casos.find(c => c.id === parseInt(btn.dataset.id));
      pedirConfirmacionEliminar(caso);
    });
  });
}

// ── Modal ─────────────────────────────────────────────────────

function abrirModal(caso = null) {
  state.editingId = caso ? caso.id : null;

  // Título y subtítulo
  document.getElementById('modal-title').textContent =
    caso ? 'Editar Caso' : 'Nuevo Caso';
  document.getElementById('modal-subtitle').textContent =
    caso ? `${caso.apellidos}, ${caso.nombre} · ${caso.dni_sip}` : 'Rellena los datos del caso';

  // Mostrar/ocultar botón eliminar
  document.getElementById('btn-eliminar').classList.toggle('hidden', !caso);

  // Resetear el formulario
  document.getElementById('caso-form').reset();

  // Si es edición, pre-rellenar todos los campos
  if (caso) {
    g('f-apellidos').value = caso.apellidos     ?? '';
    g('f-nombre').value    = caso.nombre        ?? '';
    g('f-dni').value       = caso.dni_sip       ?? '';
    g('f-zona').value      = caso.zona          ?? '';
    g('f-tel').value       = caso.telefono      ?? '';
    g('f-renov').value     = caso.mes_renovacion?? '';
    g('f-alta').value      = caso.fecha_alta    ?? '';
    g('f-baja').value      = caso.fecha_baja    ?? '';
    g('f-dir').value       = caso.direccion     ?? '';
    g('f-activo').checked  = caso.activo !== false;
    g('f-obs').value       = caso.observaciones ?? '';
    updateToggleLabel();
  }

  document.getElementById('modal-backdrop').classList.remove('hidden');
  document.getElementById('modal-submit').disabled = false;
  document.getElementById('modal-submit').textContent = 'Guardar';
  setTimeout(() => g('f-apellidos').focus(), 80);
}

function cerrarModal() {
  document.getElementById('modal-backdrop').classList.add('hidden');
  state.editingId = null;
}

/** Actualiza el texto "Activo / Baja" junto al toggle */
function updateToggleLabel() {
  const checked = g('f-activo').checked;
  document.getElementById('toggle-label-text').textContent = checked ? 'Activo' : 'Dado de baja';
  document.getElementById('toggle-label-text').style.color = checked ? 'var(--success)' : 'var(--text-3)';
}

/** Recoge los datos del formulario y los envía a la API */
async function onFormSubmit(e) {
  e.preventDefault();

  const datos = {
    apellidos:      g('f-apellidos').value.trim(),
    nombre:         g('f-nombre').value.trim(),
    dni_sip:        g('f-dni').value.trim(),
    zona:           g('f-zona').value      ? parseInt(g('f-zona').value)   : null,
    mes_renovacion: g('f-renov').value     || null,
    telefono:       g('f-tel').value.trim()  || null,
    fecha_alta:     g('f-alta').value      || null,
    fecha_baja:     g('f-baja').value      || null,
    direccion:      g('f-dir').value.trim()  || null,
    activo:         g('f-activo').checked,
    observaciones:  g('f-obs').value.trim()  || null,
  };

  // Validación mínima en el cliente
  if (!datos.apellidos || !datos.nombre || !datos.dni_sip) {
    toast('Los campos Apellidos, Nombre y DNI/SIP son obligatorios', 'error');
    return;
  }

  const submitBtn = document.getElementById('modal-submit');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Guardando...';

  try {
    if (state.editingId) {
      await actualizarCaso(state.editingId, datos);
      toast(`Caso de ${datos.apellidos} actualizado`, 'success');
    } else {
      await crearCaso(datos);
      toast(`Caso de ${datos.apellidos} creado correctamente`, 'success');
    }
    cerrarModal();
  } catch (err) {
    toast(err.message, 'error');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Guardar';
  }
}

function pedirConfirmacionEliminar(caso) {
  if (confirm(`¿Eliminar el caso de ${caso.apellidos}, ${caso.nombre}?\n\nEsta acción no se puede deshacer.`)) {
    eliminarCaso(caso.id)
      .then(() => { cerrarModal(); toast('Caso eliminado', 'info'); })
      .catch(err => toast(err.message, 'error'));
  }
}

// ── Informe PDF ───────────────────────────────────────────────

async function descargarPDF() {
  const btn = document.getElementById('btn-pdf');
  btn.disabled = true;
  btn.textContent = '⏳ Generando...';
  try {
    const res = await fetch('/mayor-a-casa/casos/informe/pdf');
    if (!res.ok) throw new Error('Error al generar el informe');
    const blob = await res.blob();
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href     = url;
    a.download = `informe_mayor_a_casa_${new Date().toISOString().slice(0, 10)}.pdf`;
    a.click();
    URL.revokeObjectURL(url);
    toast('Informe PDF descargado', 'success');
  } catch (err) {
    toast(err.message, 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>📄</span> Generar Informe PDF';
  }
}

// ── Notificaciones toast ──────────────────────────────────────

function toast(msg, type = 'info') {
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.innerHTML = `<span class="toast-icon">${icons[type] || 'ℹ'}</span><span>${msg}</span>`;
  document.getElementById('toast-container').appendChild(el);
  requestAnimationFrame(() => el.classList.add('show'));
  setTimeout(() => {
    el.classList.remove('show');
    setTimeout(() => el.remove(), 300);
  }, 3500);
}

// ── Helper: getElementById abreviado ─────────────────────────
function g(id) { return document.getElementById(id); }

// ── Inicialización ────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {

  // Cargar datos iniciales
  cargarCasos().catch(() =>
    toast('No se pudo conectar con el servidor. Comprueba que Docker está activo.', 'error')
  );

  // Botón "Nuevo caso"
  g('btn-nuevo').addEventListener('click', () => abrirModal());

  // Botón "Generar PDF"
  g('btn-pdf').addEventListener('click', descargarPDF);

  // Enviar formulario
  g('caso-form').addEventListener('submit', onFormSubmit);

  // Cerrar modal
  g('modal-close').addEventListener('click', cerrarModal);
  g('modal-cancel').addEventListener('click', cerrarModal);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') cerrarModal(); });

  // Clic fuera del modal → cerrar
  g('modal-backdrop').addEventListener('click', e => {
    if (e.target === g('modal-backdrop')) cerrarModal();
  });

  // Botón eliminar (dentro del modal)
  g('btn-eliminar').addEventListener('click', () => {
    const caso = state.casos.find(c => c.id === state.editingId);
    if (caso) pedirConfirmacionEliminar(caso);
  });

  // Toggle Activo/Baja actualiza el texto en tiempo real
  g('f-activo').addEventListener('change', updateToggleLabel);
});
