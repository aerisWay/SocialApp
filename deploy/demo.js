/* ============================================================
 * demo.js — Capa "modo demo" para la versión de portfolio (GitHub Pages)
 *
 * Se carga ANTES de app.js. Si la web NO corre en github.io (ni lleva
 * ?demo en la URL) no hace absolutamente nada, así la app real con su
 * backend FastAPI sigue funcionando igual.
 *
 * En modo demo intercepta window.fetch y responde con datos locales
 * (persistidos en localStorage), de modo que la app funciona autónoma:
 *   - Login: cualquier usuario/contraseña entra.
 *   - Casos, comisiones, facturas, seguimiento y documentación con datos
 *     de muestra (los mismos del seed de main.py).
 *   - Botones "Generar Informe PDF": descargan un PDF de demostración.
 *   - Subidas de PDF: avisan de que no están disponibles en la demo.
 * ============================================================ */
(function () {
  "use strict";

  var IS_DEMO =
    /(^|\.)github\.io$/.test(location.hostname) || /[?&]demo\b/.test(location.search);
  if (!IS_DEMO) return;

  var HOY = new Date();
  var MES_HOY = HOY.toISOString().slice(0, 7); // YYYY-MM
  var FECHA_HOY = HOY.toISOString().slice(0, 10); // YYYY-MM-DD

  // ── Datos de muestra (replican el seed de backend/app/main.py) ─────────
  // Casos: [apellidos, nombre, dni, sip, zona, sexo, rango_edad, telefono, direccion, mes_renovacion, fecha_alta, activo]
  var CASOS_RAW = [
    ["Abad Molina","Josefa","12345678A","10000001",1,"mujer","mayor_65","966 801 234","C/ Tomàs Ortuño, 12, 2ºA","2026-03","2024-01-10",true],
    ["Álvarez Campos","Manuel","23456789B","10000002",1,"hombre","mayor_65","966 802 345","Avda. del Mediterráneo, 34, 1ºB","2026-05","2023-06-15",true],
    ["Blanco Navarro","Amparo","34567890C","10000003",1,"mujer","mayor_65","966 803 456","C/ Gambo, 8, bajo","2026-07","2024-03-20",true],
    ["Cabrera Soler","Francisco","45678901D","10000004",1,"hombre","mayor_65","966 804 567","C/ La Mar, 4, 3ºA","2026-04","2022-11-05",true],
    ["Domènech Ramos","Pilar","56789012E","10000005",1,"mujer","60_65",null,"C/ Esperança, 7, 1ºC","2026-06","2023-09-12",true],
    ["Esteban Torres","Enrique","67890123F","10000006",1,"hombre","mayor_65","966 805 678","Avda. de l'Aigüera, 3, 2ºD","2026-08","2024-02-28",true],
    ["Ferrer Llopis","Carmen","78901234G","10000007",1,"mujer","mayor_65","966 806 789","C/ Ausiàs March, 11, 4ºB","2026-03","2022-07-18",false],
    ["Gómez Ibáñez","Salvador","89012345H","10000008",1,"hombre","mayor_65","966 807 890","C/ Mayor, 18, bajo B","2026-09","2023-04-01",true],
    ["Herrero Prats","Inmaculada","90123456J","10000009",1,"mujer","mayor_65","966 808 901","C/ Martínez Alejos, 5, 2ºA","2026-05","2024-01-22",true],
    ["Iglesias Vidal","Rogelio","01234567K","10000010",1,"hombre","60_65",null,"C/ Sant Vicent, 22, 1ºB","2026-07","2022-12-10",true],
    ["Jiménez Colomer","Rosa","11223344L","10000011",1,"mujer","mayor_65","966 809 012","C/ Tomàs Ortuño, 31, 3ºC","2026-04","2023-08-07",true],
    ["León Asensio","Valentina","22334455M","10000012",1,"mujer","mayor_65","966 810 123","Avda. del Mediterráneo, 67, 5ºA","2026-10","2021-05-14",true],
    ["Marín Díaz","Consuelo","33445566N","10000013",2,"no_define","menor_60","966 811 234","C/ Ibiza, 6, 2ºD","2026-08","2022-05-30",false],
    ["Martínez Blasco","Rafael","44556677P","10000014",2,"hombre","mayor_65","966 812 345","Avda. de Mallorca, 23, 1ºA","2026-03","2023-10-20",true],
    ["Navarro Ortega","Asunción","55667788Q","10000015",2,"mujer","mayor_65","966 813 456","C/ Menorca, 14, bajo A","2026-05","2024-06-01",true],
    ["Oliva Herrera","Agustín","66778899R","10000016",2,"hombre","mayor_65",null,"C/ Almeria, 9, 3ºB","2026-07","2023-02-14",true],
    ["Palomar Ruiz","Encarnación","77889900S","10000017",2,"mujer","mayor_65","966 814 567","C/ Lepanto, 17, 2ºC","2026-09","2022-09-25",true],
    ["Ramos Sánchez","Joaquín","88990011T","10000018",2,"hombre","60_65","966 815 678","C/ Formentera, 4, 1ºA","2026-04","2024-01-08",false],
    ["Reyes Gómez","Teresa","99001122V","10000019",2,"mujer","mayor_65","966 816 789","C/ Canarias, 20, 4ºD","2026-06","2023-07-17",true],
    ["Rico Ferrer","Bernardo","10112233W","10000020",2,"hombre","mayor_65","966 817 890","Avda. de Europa, 38, 3ºA","2026-08","2022-03-11",true],
    ["Romero Bernal","Gloria","21223344X","10000021",2,"mujer","mayor_65","966 818 901","C/ del Rincón de Loix, 12, 2ºB","2026-10","2021-08-22",true],
    ["Ruiz Pons","Pedro","32334455Y","10000022",2,"hombre","mayor_65",null,"C/ Martínez Alejos, 28, bajo","2026-11","2020-11-03",true],
    ["Sánchez Llobet","Dolores","43445566Z","10000023",2,"mujer","mayor_65","966 819 012","C/ Ibiza, 15, 1ºC","2026-03","2024-04-25",true],
    ["Segura Colomer","Eduardo","54556677A","10000024",2,"no_define","menor_60","966 820 123","Avda. de Mallorca, 40, 5ºB","2026-05","2023-01-30",true],
    ["Serra Campos","Francisca","65667788B","10000025",3,"mujer","mayor_65","966 821 234","C/ Menorca, 3, 2ºA","2026-07","2024-05-08",true],
    ["Soler Castillo","Ignacio","76778899C","10000026",3,"hombre","mayor_65","966 822 345","C/ Gambo, 21, 1ºD","2026-09","2022-08-19",true],
    ["Torres Morales","Montserrat","87889900D","10000027",3,"mujer","mayor_65","966 823 456","C/ Almeria, 14, 3ºC","2026-04","2023-03-05",true],
    ["Úbeda Reyes","Juan","98990011E","10000028",3,"hombre","60_65",null,"Avda. del Mediterráneo, 89, 2ºB","2026-06","2024-07-14",true],
    ["Vidal González","Natividad","09001122F","10000029",3,"mujer","mayor_65","966 824 567","C/ Lepanto, 6, bajo A","2026-08","2022-06-27",false],
    ["Villanueva Mora","Carlos","10112233G","10000030",3,"hombre","mayor_65","966 825 678","C/ Esperança, 18, 4ºA","2026-10","2021-02-08",true],
    ["Zaragoza Gil","Nieves","21223344H","10000031",3,"mujer","mayor_65","966 826 789","C/ Ausiàs March, 25, 1ºA","2026-11","2020-09-15",true],
    ["Aguilar López","Miguel","32334455J","10000032",3,"hombre","mayor_65","966 827 890","C/ La Mar, 11, 3ºB","2026-12","2020-04-20",true],
    ["Alba Moreno","Remedios","43445566K","10000033",3,"mujer","mayor_65",null,"C/ Sant Vicent, 34, 2ºC","2026-03","2024-08-11",true],
    ["Alonso Villena","Luis","54556677L","10000034",3,"hombre","menor_60","966 828 901","Avda. de l'Aigüera, 16, 5ºD","2026-05","2023-05-23",true],
    ["Ángel Gutiérrez","Socorro","65667788M","10000035",3,"mujer","mayor_65","966 829 012","C/ Mayor, 7, 1ºA","2026-07","2022-10-04",false],
    ["Arcos Roca","Santiago","76778899N","10000036",3,"hombre","mayor_65","966 830 123","C/ del Rincón de Loix, 27, bajo B","2026-09","2021-12-17",true],
    ["Arroyo Serrano","Isabel","87889900P","10000037",4,"mujer","60_65","966 831 234","C/ Formentera, 9, 2ºA","2026-04","2024-09-30",true],
    ["Aznar Mínguez","Ramón","98990011Q","10000038",4,"hombre","mayor_65","966 832 345","C/ Canarias, 8, 3ºB","2026-06","2023-11-07",true],
    ["Bravo Hidalgo","Luisa","09001122R","10000039",4,"mujer","mayor_65",null,"Avda. de Europa, 55, 1ºC","2026-08","2022-04-16",true],
    ["Bueno Climent","Pascual","10112233S","10000040",4,"hombre","mayor_65","966 833 456","Avda. de Mallorca, 12, 4ºA","2026-10","2021-07-29",true],
    ["Caballero Flores","María","21223344T","10000041",4,"mujer","mayor_65","966 834 567","C/ Gambo, 16, bajo C","2026-11","2020-06-03",false],
    ["Calvo Pastor","Marcelino","32334455V","10000042",4,"hombre","mayor_65","966 835 678","C/ Ibiza, 11, 2ºD","2026-12","2020-01-18",true],
    ["Campos Expósito","Milagros","43445566W","10000043",4,"mujer","60_65","966 836 789","C/ Menorca, 20, 3ºA","2026-03","2024-10-22",true],
    ["Cano Guerrero","Alfonso","54556677X","10000044",4,"hombre","mayor_65",null,"C/ Lepanto, 3, 1ºB","2026-05","2023-12-09",true],
    ["Castellano Castro","Petra","65667788Y","10000045",4,"no_define","mayor_65","966 837 890","C/ Ausiàs March, 38, 5ºC","2026-07","2022-02-25",true],
    ["Castro Díaz","Emilio","76778899Z","10000046",4,"hombre","mayor_65","966 838 901","C/ Tomàs Ortuño, 47, 2ºB","2026-09","2021-10-06",true],
    ["Climent Font","Serafina","87889900A","10000047",4,"mujer","mayor_65","966 839 012","Avda. del Mediterráneo, 22, 4ºD","2026-11","2020-08-13",false],
    ["Coll Rivas","Sergio","98990011B","10000048",4,"hombre","60_65","966 840 123","C/ La Mar, 18, 1ºA","2026-12","2020-03-27",true],
    ["Díaz Alvarado","Trinidad","09001122C","10000049",4,"no_define","mayor_65","966 841 234","Avda. de l'Aigüera, 9, 3ºC","2026-02","2024-11-15",true],
    ["Expósito Arroyo","Alberto","10112233D","10000050",4,"hombre","menor_60",null,"C/ Sant Vicent, 5, 2ºA","2026-04","2023-04-21",true]
  ];

  // Comisiones: [apellidos, nombre, dni, sip, zona, sexo, rango_edad, estado, mes_comision, fecha_alta]
  var COMIS_RAW = [
    ["Pérez Gómez","Antonia","11111111A","20000001",1,"mujer","mayor_65","en_tramite",MES_HOY,FECHA_HOY],
    ["García Ruiz","Manuel","22222222B","20000002",2,"hombre","60_65","en_tramite",MES_HOY,FECHA_HOY],
    ["López Sanz","Carmen","33333333C","20000003",1,"mujer","mayor_65","denegado",MES_HOY,FECHA_HOY],
    ["Sánchez Mas","Vicente","44444444D","20000004",3,"hombre","menor_60","en_tramite",MES_HOY,FECHA_HOY],
    ["Marti Bel","Rosa","55555555E","20000005",4,"mujer","mayor_65","en_tramite",MES_HOY,FECHA_HOY],
    ["Torres Vila","Josep","66666666F","20000006",2,"hombre","60_65","en_tramite",MES_HOY,FECHA_HOY],
    ["Molina Cap","Anna","77777777G","20000007",1,"mujer","mayor_65","aprobado",MES_HOY,FECHA_HOY],
    ["Vila Seco","Pere","88888888H","20000008",3,"hombre","mayor_65","en_tramite",MES_HOY,FECHA_HOY],
    ["Roca Font","Teresa","99999999J","20000009",4,"mujer","60_65","en_tramite",MES_HOY,FECHA_HOY],
    ["Soler Pau","Joan","00000000K","20000010",2,"hombre","menor_60","en_tramite",MES_HOY,FECHA_HOY],
    ["Beltran Rus","Eva","12121212A","20000011",1,"mujer","mayor_65","aprobado","2026-03","2026-03-05"],
    ["Castillo Mar","Felipe","23232323B","20000012",2,"hombre","60_65","denegado","2026-03","2026-03-10"],
    ["Duarte Sol","Sonia","34343434C","20000013",3,"mujer","menor_60","aprobado","2026-03","2026-03-15"],
    ["Esteve Pla","Ramon","45454545D","20000014",4,"hombre","mayor_65","aprobado","2026-03","2026-03-20"],
    ["Fabra Pou","Isabel","56565656E","20000015",1,"mujer","60_65","denegado","2026-03","2026-03-25"],
    ["Gallego Ros","Luis","67676767F","20000016",2,"hombre","mayor_65","aprobado","2026-02","2026-02-05"],
    ["Hidalgo Luz","Elena","78787878G","20000017",3,"mujer","menor_60","denegado","2026-02","2026-02-12"],
    ["Iborra Marí","Marc","89898989H","20000018",4,"hombre","mayor_65","aprobado","2026-02","2026-02-18"],
    ["Jover Soro","Julia","90909090J","20000019",1,"mujer","60_65","aprobado","2026-02","2026-02-22"],
    ["Lacasa Mir","Andreu","01010101K","20000020",2,"hombre","mayor_65","denegado","2026-02","2026-02-26"]
  ];

  var ANIO_ACT = HOY.getFullYear();

  function casoFromRaw(r, id) {
    return {
      id: id, apellidos: r[0], nombre: r[1], dni: r[2], sip: r[3], zona: r[4],
      sexo: r[5], rango_edad: r[6], telefono: r[7], direccion: r[8],
      mes_renovacion: r[9], fecha_alta: r[10], fecha_baja: null,
      activo: r[11], observaciones: null
    };
  }
  function comisFromRaw(r, id) {
    return {
      id: id, apellidos: r[0], nombre: r[1], dni: r[2], sip: r[3], zona: r[4],
      sexo: r[5], rango_edad: r[6], estado: r[7], mes_comision: r[8],
      fecha_alta: r[9], telefono: null, direccion: null, observaciones: null
    };
  }

  function freshDb() {
    var casos = CASOS_RAW.map(function (r, i) { return casoFromRaw(r, i + 1); });
    var comisiones = COMIS_RAW.map(function (r, i) { return comisFromRaw(r, i + 1); });
    // Facturas del año actual
    var facturas = [
      { id: 1, anio: ANIO_ACT, mes: 1, num_casos: 42, cuantia: 12600, pdf_filename: null },
      { id: 2, anio: ANIO_ACT, mes: 2, num_casos: 45, cuantia: 13500, pdf_filename: null },
      { id: 3, anio: ANIO_ACT, mes: 3, num_casos: 48, cuantia: 14400, pdf_filename: null },
      { id: 4, anio: ANIO_ACT, mes: 4, num_casos: 44, cuantia: 13200, pdf_filename: null },
      { id: 5, anio: ANIO_ACT, mes: 5, num_casos: 47, cuantia: 14100, pdf_filename: null },
      { id: 6, anio: ANIO_ACT, mes: 6, num_casos: 46, cuantia: 13800, pdf_filename: null }
    ];
    // Seguimientos del año actual
    var seguimientos = [];
    var sid = 1;
    var segSeed = {
      entrevista: [[1, 6, 4], [2, 7, 5], [3, 5, 6], [4, 8, 7]],
      visita: [[1, 4, 3], [2, 5, 4], [3, 6, 5]],
      informe: [[1, 3, 2], [2, 4, 4], [3, 5, 3]]
    };
    Object.keys(segSeed).forEach(function (tipo) {
      segSeed[tipo].forEach(function (row) {
        seguimientos.push({
          id: sid++, tipo: tipo, anio: ANIO_ACT, mes: row[0],
          cantidad: row[1] + row[2], hombres: row[1], mujeres: row[2]
        });
      });
    });
    var docs = [
      { id: 1, titulo: "Protocolo de actuación — Major a Casa 2026", pdf_filename: null },
      { id: 2, titulo: "Memoria anual del servicio", pdf_filename: null }
    ];
    return {
      casos: casos, comisiones: comisiones, facturas: facturas,
      seguimientos: seguimientos, docs: docs,
      seq: { caso: casos.length, comis: comisiones.length, factura: facturas.length, seg: seguimientos.length, doc: docs.length }
    };
  }

  // ── Almacén persistente en localStorage ───────────────────────────────
  var LS_KEY = "apbapp_demo_db_v1";
  var db;
  try {
    db = JSON.parse(localStorage.getItem(LS_KEY)) || freshDb();
  } catch (e) {
    db = freshDb();
  }
  function save() {
    try { localStorage.setItem(LS_KEY, JSON.stringify(db)); } catch (e) { /* ignore */ }
  }
  function nextId(kind) { db.seq[kind] = (db.seq[kind] || 0) + 1; return db.seq[kind]; }

  // ── Utilidades de respuesta ───────────────────────────────────────────
  function jsonRes(data, status) {
    status = status || 200;
    var body = status === 204 ? null : JSON.stringify(data);
    return new Response(body, { status: status, headers: { "Content-Type": "application/json" } });
  }
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function notify(msg) { if (typeof window.toast === "function") window.toast(msg, "info"); }

  // ── Generador de un PDF de demostración válido ────────────────────────
  function demoPdfBlob() {
    // Texto SOLO ASCII para que la longitud en caracteres == bytes (xref correcto)
    var content =
      "BT /F1 22 Tf 60 770 Td (APBApp - Informe) Tj " +
      "0 -34 Td /F1 13 Tf (Version demo de portfolio.) Tj " +
      "0 -22 Td (La generacion real de PDF requiere el backend.) Tj ET";
    var objs = [
      "<< /Type /Catalog /Pages 2 0 R >>",
      "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
      "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
      "<< /Length " + content.length + " >>\nstream\n" + content + "\nendstream",
      "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    ];
    var pdf = "%PDF-1.4\n";
    var offsets = [];
    objs.forEach(function (body, i) {
      offsets[i] = pdf.length;
      pdf += (i + 1) + " 0 obj\n" + body + "\nendobj\n";
    });
    var xrefStart = pdf.length;
    pdf += "xref\n0 " + (objs.length + 1) + "\n0000000000 65535 f \n";
    offsets.forEach(function (off) {
      pdf += ("0000000000" + off).slice(-10) + " 00000 n \n";
    });
    pdf += "trailer\n<< /Size " + (objs.length + 1) + " /Root 1 0 R >>\nstartxref\n" + xrefStart + "\n%%EOF";
    return new Blob([pdf], { type: "application/pdf" });
  }
  function pdfRes() {
    return new Response(demoPdfBlob(), { status: 200, headers: { "Content-Type": "application/pdf" } });
  }

  // ── Enrutador del modo demo ───────────────────────────────────────────
  function handle(method, path, search, body) {
    // Informes PDF (cualquier recurso) → PDF de demostración
    if (/\/informe\/pdf(\/|$)/.test(path)) return pdfRes();

    if (path === "/auth/login" && method === "POST") {
      return jsonRes({ access_token: "demo-token", dept_name: "Servicio de Promoción" });
    }

    var m;

    // ── Casos ──
    if (path === "/mayor-a-casa/casos/") {
      if (method === "GET") return jsonRes(db.casos);
      if (method === "POST") {
        var c = Object.assign({ id: nextId("caso") }, body, { fecha_baja: body.fecha_baja || null });
        db.casos.push(c); save(); return jsonRes(c, 201);
      }
    }
    if ((m = path.match(/^\/mayor-a-casa\/casos\/(\d+)$/))) {
      var ci = db.casos.findIndex(function (x) { return x.id === +m[1]; });
      if (ci < 0) return jsonRes({ detail: "No encontrado" }, 404);
      if (method === "PATCH") { db.casos[ci] = Object.assign({}, db.casos[ci], body); save(); return jsonRes(db.casos[ci]); }
      if (method === "DELETE") { db.casos.splice(ci, 1); save(); return jsonRes(null, 204); }
    }

    // ── Comisiones ──
    if (path === "/mayor-a-casa/comisiones/") {
      if (method === "GET") return jsonRes(db.comisiones);
      if (method === "POST") {
        var co = Object.assign({ id: nextId("comis") }, body);
        db.comisiones.push(co); save(); return jsonRes(co, 201);
      }
    }
    if ((m = path.match(/^\/mayor-a-casa\/comisiones\/(\d+)\/aprobar$/)) && method === "POST") {
      var xi = db.comisiones.findIndex(function (x) { return x.id === +m[1]; });
      if (xi < 0) return jsonRes({ detail: "No encontrado" }, 404);
      var com = db.comisiones[xi];
      var nuevo = {
        id: nextId("caso"), apellidos: com.apellidos, nombre: com.nombre, dni: com.dni,
        sip: com.sip, zona: com.zona, sexo: com.sexo, rango_edad: com.rango_edad,
        telefono: null, direccion: null, mes_renovacion: null,
        fecha_alta: FECHA_HOY, fecha_baja: null, activo: true, observaciones: null
      };
      db.casos.push(nuevo);
      db.comisiones.splice(xi, 1);
      save();
      return jsonRes(nuevo, 201);
    }
    if ((m = path.match(/^\/mayor-a-casa\/comisiones\/(\d+)$/))) {
      var coi = db.comisiones.findIndex(function (x) { return x.id === +m[1]; });
      if (coi < 0) return jsonRes({ detail: "No encontrado" }, 404);
      if (method === "PATCH") { db.comisiones[coi] = Object.assign({}, db.comisiones[coi], body); save(); return jsonRes(db.comisiones[coi]); }
      if (method === "DELETE") { db.comisiones.splice(coi, 1); save(); return jsonRes(null, 204); }
    }

    // ── Facturas ──
    if (path === "/mayor-a-casa/facturas/") {
      if (method === "GET") {
        var anio = +(search.get("anio") || ANIO_ACT);
        return jsonRes(db.facturas.filter(function (f) { return f.anio === anio; }));
      }
      if (method === "PUT") {
        var fi = db.facturas.findIndex(function (f) { return f.anio === body.anio && f.mes === body.mes; });
        if (fi >= 0) { db.facturas[fi] = Object.assign({}, db.facturas[fi], body); }
        else { db.facturas.push(Object.assign({ id: nextId("factura"), pdf_filename: null }, body)); fi = db.facturas.length - 1; }
        save(); return jsonRes(db.facturas[fi]);
      }
    }
    if ((m = path.match(/^\/mayor-a-casa\/facturas\/(\d+)\/pdf$/))) {
      if (method === "POST") { notify("Subir PDF no está disponible en la versión demo."); return jsonRes({ pdf_filename: null }); }
      if (method === "DELETE") {
        var fp = db.facturas.findIndex(function (f) { return f.id === +m[1]; });
        if (fp >= 0) { db.facturas[fp].pdf_filename = null; save(); }
        return jsonRes(null, 204);
      }
    }

    // ── Seguimientos ──
    if (path === "/mayor-a-casa/seguimientos/") {
      if (method === "GET") {
        var sa = +(search.get("anio") || ANIO_ACT);
        return jsonRes(db.seguimientos.filter(function (s) { return s.anio === sa; }));
      }
      if (method === "PUT") {
        var si = db.seguimientos.findIndex(function (s) { return s.tipo === body.tipo && s.anio === body.anio && s.mes === body.mes; });
        if (si >= 0) { db.seguimientos[si] = Object.assign({}, db.seguimientos[si], body); }
        else { db.seguimientos.push(Object.assign({ id: nextId("seg"), cantidad: null, hombres: null, mujeres: null }, body)); si = db.seguimientos.length - 1; }
        save(); return jsonRes(db.seguimientos[si]);
      }
    }

    // ── Documentación ──
    if (path === "/mayor-a-casa/documentacion/") {
      if (method === "GET") return jsonRes(db.docs);
      if (method === "POST") { var d = { id: nextId("doc"), titulo: body.titulo, pdf_filename: null }; db.docs.push(d); save(); return jsonRes(d, 201); }
    }
    if ((m = path.match(/^\/mayor-a-casa\/documentacion\/(\d+)\/pdf$/))) {
      if (method === "POST") { notify("Subir PDF no está disponible en la versión demo."); return jsonRes({ pdf_filename: null }); }
      if (method === "DELETE") {
        var dp = db.docs.findIndex(function (x) { return x.id === +m[1]; });
        if (dp >= 0) { db.docs[dp].pdf_filename = null; save(); }
        return jsonRes(null, 204);
      }
    }
    if ((m = path.match(/^\/mayor-a-casa\/documentacion\/(\d+)$/))) {
      var di = db.docs.findIndex(function (x) { return x.id === +m[1]; });
      if (di < 0) return jsonRes({ detail: "No encontrado" }, 404);
      if (method === "PATCH") { db.docs[di] = Object.assign({}, db.docs[di], body); save(); return jsonRes(db.docs[di]); }
      if (method === "DELETE") { db.docs.splice(di, 1); save(); return jsonRes(null, 204); }
    }

    return jsonRes({ detail: "Recurso no disponible en la demo" }, 404);
  }

  // ── Intercepción de window.fetch ──────────────────────────────────────
  var realFetch = window.fetch ? window.fetch.bind(window) : null;
  window.fetch = async function (input, init) {
    init = init || {};
    var url = typeof input === "string" ? input : (input && input.url) || "";
    var path, search;
    try {
      var u = new URL(url, location.origin);
      path = u.pathname;
      search = u.searchParams;
    } catch (e) {
      return realFetch ? realFetch(input, init) : Promise.reject(e);
    }

    // Solo interceptamos las rutas de la API de la app
    if (!/^\/(auth|mayor-a-casa)\//.test(path)) {
      return realFetch ? realFetch(input, init) : Promise.reject(new Error("offline"));
    }

    var method = (init.method || (typeof input !== "string" && input && input.method) || "GET").toUpperCase();
    var body = null;
    if (init.body && typeof init.body === "string") {
      try { body = JSON.parse(init.body); } catch (e) { body = null; }
    }

    await sleep(140); // pequeña latencia para que se vean los spinners
    try {
      return handle(method, path, search, body || {});
    } catch (e) {
      return jsonRes({ detail: e.message || "Error demo" }, 400);
    }
  };

  // ── Pista visual en la pantalla de login ──────────────────────────────
  function injectLoginHint() {
    var form = document.getElementById("login-form");
    if (!form || document.getElementById("demo-hint")) return;
    var user = document.getElementById("login-user");
    var pass = document.getElementById("login-pass");
    if (user && !user.value) user.value = "demo";
    if (pass && !pass.value) pass.value = "demo";
    var hint = document.createElement("p");
    hint.id = "demo-hint";
    hint.style.cssText =
      "margin-top:14px;padding:10px 12px;border-radius:8px;font-size:13px;line-height:1.4;" +
      "text-align:center;background:rgba(99,102,241,.12);color:#a5b4fc;border:1px solid rgba(99,102,241,.3);";
    hint.innerHTML =
      "🔓 <strong>Versión demo</strong> — entra con <strong>cualquier</strong> usuario y contraseña.<br>" +
      "Datos de ejemplo · sin conexión a backend.";
    form.appendChild(hint);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectLoginHint);
  } else {
    injectLoginHint();
  }

  console.info("[APBApp] Modo demo activo — fetch interceptado, datos locales.");
})();
