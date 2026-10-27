import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import {
  obtenerTableroAdmin,
  type EstadoServicio,
  type TableroAdminOut,
  type Usuario,
} from "../api";
import { lugarDe, type Lugar } from "../herramientas";
import { useSesion } from "../sesion";

type Metrica = {
  etiqueta: string;
  detalle: string;
};

type Panel = {
  titulo: string;
  columnas: string[];
  vacio: string;
};

const tablerosRol: Record<Exclude<Lugar, "administrador">, { metricas: Metrica[]; paneles: Panel[] }> = {
  cliente: {
    metricas: [
      { etiqueta: "Solicitudes abiertas", detalle: "Publicadas y sin cotización elegida" },
      { etiqueta: "Cotizaciones por elegir", detalle: "Enviadas y todavía abiertas" },
      { etiqueta: "Servicios en seguimiento", detalle: "Pendiente, en curso o por historial" },
      { etiqueta: "Servicios cerrados", detalle: "Quedan en el historial" },
    ],
    paneles: [
      {
        titulo: "Solicitudes abiertas",
        columnas: ["Título", "Categoría", "Estado"],
        vacio: "No tienes solicitudes abiertas.",
      },
      {
        titulo: "Cotizaciones por elegir",
        columnas: ["Proveedor", "Estado"],
        vacio: "No hay cotizaciones enviadas.",
      },
      {
        titulo: "Servicios en seguimiento",
        columnas: ["Servicio", "Estado"],
        vacio: "No hay un servicio activo.",
      },
    ],
  },
  administrativo: {
    metricas: [
      { etiqueta: "Por decidir", detalle: "Solicitudes que tu perfil aún no responde" },
      { etiqueta: "Plazo de cotización", detalle: "Aceptadas, dentro de las 24 horas" },
      { etiqueta: "Servicios del perfil", detalle: "Asignados a tu organización" },
      { etiqueta: "Por cerrar", detalle: "Pendientes de historial" },
    ],
    paneles: [
      {
        titulo: "Por decidir",
        columnas: ["Solicitud", "Categoría"],
        vacio: "No hay solicitudes pendientes de tu perfil.",
      },
      {
        titulo: "Dentro de las 24 horas",
        columnas: ["Solicitud", "Plazo"],
        vacio: "Ninguna aceptación está dentro del plazo.",
      },
      {
        titulo: "Servicios del perfil",
        columnas: ["Servicio", "Estado", "Técnico"],
        vacio: "No hay servicios asignados.",
      },
    ],
  },
  tecnico: {
    metricas: [
      { etiqueta: "Asignados", detalle: "Servicios en los que realizas el trabajo" },
      { etiqueta: "En curso", detalle: "El trabajo ya empezó" },
      { etiqueta: "Por historial", detalle: "Falta el registro para cerrar" },
      { etiqueta: "Captura", detalle: "Voz en campo con dispositivo autorizado" },
    ],
    paneles: [
      {
        titulo: "Servicios asignados",
        columnas: ["Servicio", "Estado"],
        vacio: "No tienes un servicio asignado.",
      },
      {
        titulo: "Pendiente de historial",
        columnas: ["Servicio", "Fecha"],
        vacio: "Nada esperando el registro de cierre.",
      },
      {
        titulo: "Captura en campo",
        columnas: ["Dispositivo", "Estado"],
        vacio: "Sin captura de un dispositivo autorizado.",
      },
    ],
  },
};

const KPI_VACIO: TableroAdminOut = {
  kpis: {
    solicitudes_abiertas: 0,
    solicitudes_sin_cotizacion: 0,
    solicitudes_rezagadas_24h: 0,
    solicitudes_dirigidas_abiertas: 0,
    solicitudes_con_cotizacion_por_elegir: 0,
    participaciones_en_plazo: 0,
    participaciones_por_vencer_6h: 0,
    participaciones_vencidas_total: 0,
    cotizaciones_enviadas_activas: 0,
    servicios_activos: 0,
    servicios_sin_tecnico: 0,
    servicios_en_curso: 0,
    servicios_pendiente_historial: 0,
    servicios_cerrados: 0,
    servicios_cancelados: 0,
    perfiles_bloqueados: 0,
    perfiles_en_riesgo: 0,
    proveedores_reincidentes_vencimiento: 0,
    marcas_totales: 0,
    promedio_calificacion: null,
    calificaciones_totales: 0,
    calificaciones_manuales: 0,
    calificaciones_automaticas_45: 0,
    calificaciones_bajas: 0,
    clientes_activos: 0,
    proveedores_activos: 0,
    usuarios_administrativos: 0,
    usuarios_tecnicos: 0,
    dispositivos_esp32: 0,
    cuentas_en_baja: 0,
  },
  vigilancia: [],
  solicitudes_atencion: [],
  servicios_activos: [],
  cobertura_categorias: [],
  padron_reciente: [],
};

export function Inicio() {
  const { usuario, listo } = useSesion();
  if (!listo) return <p className="ayuda">Cargando…</p>;
  if (!usuario) return <Navigate to="/" replace />;

  const lugar = lugarDe(usuario);
  const ahora = new Date();

  if (lugar === "administrador") {
    return <TableroAdministrador usuario={usuario} ahora={ahora} />;
  }

  const tablero = tablerosRol[lugar];
  const [principal, ...lateral] = tablero.paneles;

  return (
    <section className="tablero">
      <header className="tablero-encabezado">
        <div>
          <p className="kicker">{etiqueta(usuario)}</p>
          <h1>
            {saludo(ahora)}, {usuario.nombre}
          </h1>
        </div>
        <p className="tablero-fecha">{fechaLegible(ahora)}</p>
      </header>
      <div className="metricas">
        {tablero.metricas.map((metrica) => (
          <article key={metrica.etiqueta} className="metrica">
            <span>{metrica.etiqueta}</span>
            <strong>—</strong>
            <p>{metrica.detalle}</p>
          </article>
        ))}
      </div>
      <div className="tablero-cuerpo">
        <PanelOperacion panel={principal} />
        <div className="tablero-lateral">
          {lateral.map((panel) => (
            <PanelOperacion key={panel.titulo} panel={panel} />
          ))}
        </div>
      </div>
    </section>
  );
}

function TableroAdministrador({ usuario, ahora }: { usuario: Usuario; ahora: Date }) {
  const [datos, setDatos] = useState<TableroAdminOut>(KPI_VACIO);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let activo = true;
    obtenerTableroAdmin()
      .then((respuesta) => {
        if (!activo) return;
        setDatos(respuesta);
        setCargando(false);
      })
      .catch((causa) => {
        if (!activo) return;
        setError(causa instanceof Error ? causa.message : "No se pudo consultar el estado del sistema");
        setCargando(false);
      });
    return () => {
      activo = false;
    };
  }, []);

  const { kpis } = datos;
  const categoriasSinProveedor = datos.cobertura_categorias.filter((c) => c.sin_cobertura).length;
  const alertasCriticas =
    kpis.perfiles_bloqueados +
    kpis.solicitudes_rezagadas_24h +
    kpis.servicios_pendiente_historial +
    categoriasSinProveedor;

  const etapasEmbudo = [
    {
      etapa: "1. Sin cotización",
      valor: kpis.solicitudes_sin_cotizacion,
      detalle:
        kpis.solicitudes_rezagadas_24h > 0
          ? `${kpis.solicitudes_rezagadas_24h} con más de 24 h abiertas`
          : "Esperando aceptación de proveedores",
      alerta: kpis.solicitudes_rezagadas_24h > 0,
    },
    {
      etapa: "2. En plazo de 24 h",
      valor: kpis.participaciones_en_plazo,
      detalle:
        kpis.participaciones_por_vencer_6h > 0
          ? `${kpis.participaciones_por_vencer_6h} por vencer en ≤6 h`
          : "Aceptadas sin reservar solicitud",
      alerta: kpis.participaciones_por_vencer_6h > 0,
    },
    {
      etapa: "3. Por elegir cliente",
      valor: kpis.solicitudes_con_cotizacion_por_elegir,
      detalle: `${kpis.cotizaciones_enviadas_activas} cotizaciones enviadas vigentes`,
      alerta: false,
    },
    {
      etapa: "4. En ejecución",
      valor: kpis.servicios_sin_tecnico + kpis.servicios_en_curso,
      detalle: `${kpis.servicios_sin_tecnico} sin técnico · ${kpis.servicios_en_curso} en curso`,
      alerta: kpis.servicios_sin_tecnico > 0,
    },
    {
      etapa: "5. Falta historial",
      valor: kpis.servicios_pendiente_historial,
      detalle: "Ya no cancelables; exigen registro",
      alerta: kpis.servicios_pendiente_historial > 0,
    },
    {
      etapa: "6. Servicios cerrados",
      valor: kpis.servicios_cerrados,
      detalle: `${kpis.servicios_cancelados} cancelados acumulados`,
      alerta: false,
    },
  ];

  const porcentajeManual =
    kpis.calificaciones_totales > 0
      ? Math.round((kpis.calificaciones_manuales / kpis.calificaciones_totales) * 100)
      : null;

  return (
    <section className="tablero tablero-admin">
      <header className="tablero-encabezado">
        <div>
          <p className="kicker">{etiqueta(usuario)}</p>
          <h1>
            {saludo(ahora)}, {usuario.nombre}
          </h1>
          <p className="tablero-subtitulo">
            Supervisión de intermediación, plazos de 24 horas, cierres de historial, disciplina y cobertura de proveedores.
          </p>
        </div>
        <div className="tablero-meta">
          <p className="tablero-fecha">{fechaLegible(ahora)}</p>
          <span className={alertasCriticas > 0 ? "estado-pulso estado-alerta" : "estado-pulso estado-ok"}>
            {cargando
              ? "Sincronizando indicadores…"
              : alertasCriticas > 0
                ? `${alertasCriticas} punto(s) requieren atención`
                : "Sin bloqueos ni rezagos críticos"}
          </span>
        </div>
      </header>

      {error ? <p className="error">{error}</p> : null}

      <div className="metricas metricas-admin" aria-label="Indicadores clave de la plataforma">
        <article className="metrica metrica-admin">
          <div className="metrica-cabecera">
            <span>Demanda y meta &lt; 24 h</span>
            <span className={kpis.solicitudes_rezagadas_24h > 0 ? "insignia insignia-alerta" : "insignia"}>
              {kpis.solicitudes_rezagadas_24h > 0
                ? `${kpis.solicitudes_rezagadas_24h} rezagada(s) >24 h`
                : "En tiempo"}
            </span>
          </div>
          <strong>{cargando ? "—" : kpis.solicitudes_abiertas}</strong>
          <p>Solicitudes abiertas en el mercado</p>
          <dl className="metrica-desglose">
            <div>
              <dt>Sin cotizar</dt>
              <dd>{kpis.solicitudes_sin_cotizacion}</dd>
            </div>
            <div>
              <dt>Por elegir</dt>
              <dd>{kpis.solicitudes_con_cotizacion_por_elegir}</dd>
            </div>
            <div>
              <dt>Dirigidas</dt>
              <dd>{kpis.solicitudes_dirigidas_abiertas}</dd>
            </div>
          </dl>
        </article>

        <article className="metrica metrica-admin">
          <div className="metrica-cabecera">
            <span>Reloj de cotización (24 h)</span>
            <span
              className={
                kpis.participaciones_por_vencer_6h > 0 || kpis.participaciones_vencidas_total > 0
                  ? "insignia insignia-aviso"
                  : "insignia"
              }
            >
              {kpis.participaciones_vencidas_total} vencida(s)
            </span>
          </div>
          <strong>{cargando ? "—" : kpis.participaciones_en_plazo}</strong>
          <p>Participaciones aceptadas con plazo activo</p>
          <dl className="metrica-desglose">
            <div>
              <dt>Vencen ≤6 h</dt>
              <dd>{kpis.participaciones_por_vencer_6h}</dd>
            </div>
            <div>
              <dt>Propuestas</dt>
              <dd>{kpis.cotizaciones_enviadas_activas}</dd>
            </div>
            <div>
              <dt>Reincidentes</dt>
              <dd>{kpis.proveedores_reincidentes_vencimiento}</dd>
            </div>
          </dl>
        </article>

        <article className="metrica metrica-admin">
          <div className="metrica-cabecera">
            <span>Ejecución e historial</span>
            <span
              className={
                kpis.servicios_pendiente_historial > 0 || kpis.servicios_sin_tecnico > 0
                  ? "insignia insignia-aviso"
                  : "insignia"
              }
            >
              {kpis.servicios_pendiente_historial} por documentar
            </span>
          </div>
          <strong>{cargando ? "—" : kpis.servicios_activos}</strong>
          <p>Servicios activos en seguimiento</p>
          <dl className="metrica-desglose">
            <div>
              <dt>Sin técnico</dt>
              <dd>{kpis.servicios_sin_tecnico}</dd>
            </div>
            <div>
              <dt>En curso</dt>
              <dd>{kpis.servicios_en_curso}</dd>
            </div>
            <div>
              <dt>Cerrados</dt>
              <dd>{kpis.servicios_cerrados}</dd>
            </div>
          </dl>
        </article>

        <article className="metrica metrica-admin">
          <div className="metrica-cabecera">
            <span>Disciplina y bloqueos</span>
            <span
              className={
                kpis.perfiles_bloqueados > 0
                  ? "insignia insignia-alerta"
                  : kpis.perfiles_en_riesgo > 0
                    ? "insignia insignia-aviso"
                    : "insignia"
              }
            >
              {kpis.perfiles_en_riesgo} en 2/3 marcas
            </span>
          </div>
          <strong>{cargando ? "—" : kpis.perfiles_bloqueados}</strong>
          <p>Perfiles bloqueados (3 marcas distintas)</p>
          <dl className="metrica-desglose">
            <div>
              <dt>En riesgo (2/3)</dt>
              <dd>{kpis.perfiles_en_riesgo}</dd>
            </div>
            <div>
              <dt>Marcas emitidas</dt>
              <dd>{kpis.marcas_totales}</dd>
            </div>
            <div>
              <dt>Por vencimiento</dt>
              <dd>{kpis.proveedores_reincidentes_vencimiento}</dd>
            </div>
          </dl>
        </article>

        <article className="metrica metrica-admin">
          <div className="metrica-cabecera">
            <span>Calificación mutua</span>
            <span className={kpis.calificaciones_bajas > 0 ? "insignia insignia-aviso" : "insignia"}>
              {porcentajeManual !== null ? `${porcentajeManual}% manual` : "Escala 1 a 5"}
            </span>
          </div>
          <strong>
            {cargando
              ? "—"
              : kpis.promedio_calificacion !== null
                ? `${kpis.promedio_calificacion.toFixed(1)} ★`
                : "Sin cierres"}
          </strong>
          <p>Nota media fija al cierre (4.5 si se omite)</p>
          <dl className="metrica-desglose">
            <div>
              <dt>Manuales</dt>
              <dd>{kpis.calificaciones_manuales}</dd>
            </div>
            <div>
              <dt>Auto (4.5)</dt>
              <dd>{kpis.calificaciones_automaticas_45}</dd>
            </div>
            <div>
              <dt>Bajas (≤3.0)</dt>
              <dd>{kpis.calificaciones_bajas}</dd>
            </div>
          </dl>
        </article>

        <article className="metrica metrica-admin">
          <div className="metrica-cabecera">
            <span>Padrón y cobertura</span>
            <span className={categoriasSinProveedor > 0 ? "insignia insignia-alerta" : "insignia"}>
              {categoriasSinProveedor > 0
                ? `${categoriasSinProveedor} cat. sin soporte`
                : `${datos.cobertura_categorias.length} cat. cubiertas`}
            </span>
          </div>
          <strong>{cargando ? "—" : kpis.clientes_activos + kpis.proveedores_activos}</strong>
          <p>Perfiles activos dados de alta por Nexora</p>
          <dl className="metrica-desglose">
            <div>
              <dt>Clientes / Prov.</dt>
              <dd>
                {kpis.clientes_activos} / {kpis.proveedores_activos}
              </dd>
            </div>
            <div>
              <dt>Téc. / Admin</dt>
              <dd>
                {kpis.usuarios_tecnicos} / {kpis.usuarios_administrativos}
              </dd>
            </div>
            <div>
              <dt>ESP32 / Bajas</dt>
              <dd>
                {kpis.dispositivos_esp32} / {kpis.cuentas_en_baja}
              </dd>
            </div>
          </dl>
        </article>
      </div>

      <section className="panel-dash panel-embudo" aria-label="Flujo de intermediación">
        <div className="panel-cabecera">
          <div>
            <h2>Embudo de intermediación en tiempo real</h2>
            <p className="panel-nota">
              Recorrido desde la solicitud abierta hasta el cierre con historial obligatorio y calificación mutua.
            </p>
          </div>
        </div>
        <ol className="embudo-pasos">
          {etapasEmbudo.map((paso) => (
            <li
              key={paso.etapa}
              className={paso.alerta ? "embudo-paso embudo-paso-alerta" : "embudo-paso"}
            >
              <span className="embudo-etiqueta">{paso.etapa}</span>
              <strong className="embudo-valor">{cargando ? "—" : paso.valor}</strong>
              <span className="embudo-detalle">{paso.detalle}</span>
            </li>
          ))}
        </ol>
      </section>

      <div className="tablero-cuerpo tablero-cuerpo-admin">
        <div className="tablero-columna-principal">
          <section className="panel-dash">
            <div className="panel-cabecera">
              <div>
                <h2>Vigilancia de sanciones, bloqueos y vencimientos de 24 h</h2>
                <p className="panel-nota">
                  Tres marcas distintas bloquean al perfil. El desbloqueo lo aplica Nexora sin reiniciar el conteo; el historial solo se consulta al atender una marca, bloqueo o reclamación (auditable).
                </p>
              </div>
            </div>
            <table>
              <thead>
                <tr>
                  <th scope="col">Perfil</th>
                  <th scope="col">Marcas</th>
                  <th scope="col">Vencimientos 24 h</th>
                  <th scope="col">Estado / Motivo de atención</th>
                </tr>
              </thead>
              <tbody>
                {datos.vigilancia.length === 0 ? (
                  <tr>
                    <td colSpan={4}>
                      Sin perfiles bloqueados, en umbral de 2 marcas ni con vencimientos de 24 horas acumulados.
                    </td>
                  </tr>
                ) : (
                  datos.vigilancia.map((item) => (
                    <tr key={item.perfil_id}>
                      <td>
                        <strong className="celda-titulo">{item.nombre}</strong>
                        <span className="celda-sub">{item.tipo_perfil}</span>
                      </td>
                      <td>
                        <span
                          className={
                            item.bloqueado
                              ? "insignia insignia-alerta"
                              : item.conteo_marcas >= 2
                                ? "insignia insignia-aviso"
                                : "insignia"
                          }
                        >
                          {item.conteo_marcas} / 3
                        </span>
                      </td>
                      <td>{item.vencimientos_24h > 0 ? `${item.vencimientos_24h} sin cotizar` : "0"}</td>
                      <td>
                        <span className="celda-titulo">{item.motivo_atencion}</span>
                        {item.ultima_causa ? (
                          <span className="celda-sub">Última causa: {item.ultima_causa}</span>
                        ) : null}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </section>

          <section className="panel-dash">
            <div className="panel-cabecera">
              <div>
                <h2>Solicitudes abiertas y plazos de 24 horas</h2>
                <p className="panel-nota">
                  Aceptar no aparta la solicitud. Si pasan 24 horas sin cotizar, la participación vence y la solicitud sigue abierta.
                </p>
              </div>
            </div>
            <table>
              <thead>
                <tr>
                  <th scope="col">Solicitud / Cliente</th>
                  <th scope="col">Categoría / Modalidad</th>
                  <th scope="col">Plazos 24 h</th>
                  <th scope="col">Cotizaciones</th>
                  <th scope="col">Tiempo abierta</th>
                </tr>
              </thead>
              <tbody>
                {datos.solicitudes_atencion.length === 0 ? (
                  <tr>
                    <td colSpan={5}>No hay solicitudes abiertas pendientes de cotización o elección.</td>
                  </tr>
                ) : (
                  datos.solicitudes_atencion.map((sol) => (
                    <tr key={sol.id}>
                      <td>
                        <strong className="celda-titulo">{sol.titulo}</strong>
                        <span className="celda-sub">{sol.cliente}</span>
                      </td>
                      <td>
                        <span className="celda-titulo">{sol.categoria}</span>
                        <span className="celda-sub">
                          {sol.es_dirigida ? "Dirigida (recontratación)" : "Abierta al padrón"}
                        </span>
                      </td>
                      <td>
                        <span className="celda-titulo">
                          {sol.aceptadas_en_plazo > 0
                            ? `${sol.aceptadas_en_plazo} en plazo${
                                sol.horas_restantes_plazo_min !== null
                                  ? ` (mín. ${sol.horas_restantes_plazo_min} h)`
                                  : ""
                              }`
                            : "Sin aceptación activa"}
                        </span>
                        {sol.vencidas > 0 ? (
                          <span className="celda-sub">{sol.vencidas} participación(es) vencida(s)</span>
                        ) : null}
                      </td>
                      <td>
                        <span
                          className={
                            sol.cotizaciones_enviadas > 0 ? "insignia insignia-ok" : "insignia"
                          }
                        >
                          {sol.cotizaciones_enviadas} enviada(s)
                        </span>
                      </td>
                      <td>
                        <span
                          className={sol.rezagada_24h ? "insignia insignia-alerta" : "insignia"}
                        >
                          {sol.horas_abierta} h{sol.rezagada_24h ? " · >24 h sin cotizar" : ""}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </section>

          <section className="panel-dash">
            <div className="panel-cabecera">
              <div>
                <h2>Servicios activos y requerimiento de cierre</h2>
                <p className="panel-nota">
                  Antes de pasar a en curso debe haber técnico asignado. Desde pendiente de historial ya no se cancela: exige documentar lo realizado para cerrar.
                </p>
              </div>
            </div>
            <table>
              <thead>
                <tr>
                  <th scope="col">Servicio</th>
                  <th scope="col">Proveedor / Técnico</th>
                  <th scope="col">Estado</th>
                  <th scope="col">Condición operativa</th>
                </tr>
              </thead>
              <tbody>
                {datos.servicios_activos.length === 0 ? (
                  <tr>
                    <td colSpan={4}>
                      No hay servicios en estado pendiente, en curso o esperando registro de historial.
                    </td>
                  </tr>
                ) : (
                  datos.servicios_activos.map((srv) => (
                    <tr key={srv.id}>
                      <td>
                        <strong className="celda-titulo">{srv.solicitud_titulo}</strong>
                      </td>
                      <td>
                        <span className="celda-titulo">{srv.proveedor}</span>
                        <span className="celda-sub">
                          {srv.tecnico ? `Técnico: ${srv.tecnico}` : "Sin técnico asignado"}
                        </span>
                      </td>
                      <td>
                        <span className={claseEstadoServicio(srv.estado)}>
                          {etiquetaEstadoServicio(srv.estado)}
                        </span>
                      </td>
                      <td>{srv.requisito_avance}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </section>
        </div>

        <div className="tablero-lateral">
          <section className="panel-dash">
            <div className="panel-cabecera">
              <div>
                <h2>Cobertura de soporte por categoría</h2>
                <p className="panel-nota">
                  Meta: que el 100 % de las solicitudes cuenten con al menos un proveedor activo en su categoría.
                </p>
              </div>
            </div>
            <table>
              <thead>
                <tr>
                  <th scope="col">Categoría</th>
                  <th scope="col">Proveedores</th>
                  <th scope="col">Abiertas</th>
                  <th scope="col">Estado</th>
                </tr>
              </thead>
              <tbody>
                {datos.cobertura_categorias.length === 0 ? (
                  <tr>
                    <td colSpan={4}>
                      Aún no hay categorías registradas. Se crean al dar de alta perfiles proveedor.
                    </td>
                  </tr>
                ) : (
                  datos.cobertura_categorias.map((cat) => (
                    <tr key={cat.id}>
                      <td>
                        <strong className="celda-titulo">{cat.nombre}</strong>
                      </td>
                      <td>{cat.proveedores_activos}</td>
                      <td>{cat.solicitudes_abiertas}</td>
                      <td>
                        <span
                          className={
                            cat.sin_cobertura ? "insignia insignia-alerta" : "insignia insignia-ok"
                          }
                        >
                          {cat.sin_cobertura ? "Sin proveedor activo" : "Cubierta"}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </section>

          <section className="panel-dash">
            <div className="panel-cabecera">
              <div>
                <h2>Últimas altas en el padrón</h2>
                <p className="panel-nota">
                  Perfiles cliente y proveedor registrados por administración. Las bajas se depuran a los 12 meses ({kpis.cuentas_en_baja} en retención).
                </p>
              </div>
            </div>
            <table>
              <thead>
                <tr>
                  <th scope="col">Perfil</th>
                  <th scope="col">Rol / Tipo</th>
                  <th scope="col">Ubicación y alcance</th>
                </tr>
              </thead>
              <tbody>
                {datos.padron_reciente.length === 0 ? (
                  <tr>
                    <td colSpan={3}>No hay perfiles cliente ni proveedor dados de alta todavía.</td>
                  </tr>
                ) : (
                  datos.padron_reciente.map((item) => (
                    <tr key={item.perfil_id}>
                      <td>
                        <strong className="celda-titulo">{item.nombre}</strong>
                        {item.bloqueado ? (
                          <span className="insignia insignia-alerta">Bloqueado</span>
                        ) : null}
                      </td>
                      <td>
                        <span className="celda-titulo">{item.rol}</span>
                        <span className="celda-sub">{item.subtipo}</span>
                      </td>
                      <td>
                        <span className="celda-titulo">{item.ubicacion}</span>
                        <span className="celda-sub">{item.detalle}</span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </section>
        </div>
      </div>
    </section>
  );
}

function PanelOperacion({ panel }: { panel: Panel }) {
  return (
    <section className="panel-dash">
      <h2>{panel.titulo}</h2>
      <table>
        <thead>
          <tr>
            {panel.columnas.map((columna) => (
              <th key={columna} scope="col">
                {columna}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colSpan={panel.columnas.length}>{panel.vacio}</td>
          </tr>
        </tbody>
      </table>
    </section>
  );
}

function etiquetaEstadoServicio(estado: EstadoServicio): string {
  if (estado === "pendiente") return "Pendiente";
  if (estado === "en_curso") return "En curso";
  if (estado === "pendiente_historial") return "Pendiente de historial";
  if (estado === "cerrado") return "Cerrado";
  return "Cancelado";
}

function claseEstadoServicio(estado: EstadoServicio): string {
  if (estado === "pendiente_historial") return "insignia insignia-aviso";
  if (estado === "en_curso") return "insignia insignia-ok";
  return "insignia";
}

function etiqueta(usuario: Usuario): string {
  if (usuario.tipo_cuenta === "cliente") return "Cliente";
  if (usuario.tipo_cuenta === "administrador") return "Administrador de plataforma";
  if (usuario.funcion === "tecnico") return "Técnico";
  return "Administrativo del proveedor";
}

function saludo(fecha: Date): string {
  const hora = fecha.getHours();
  if (hora < 12) return "Buenos días";
  if (hora < 19) return "Buenas tardes";
  return "Buenas noches";
}

function fechaLegible(fecha: Date): string {
  const texto = new Intl.DateTimeFormat("es-MX", {
    weekday: "long",
    day: "numeric",
    month: "long",
  }).format(fecha);
  return texto.charAt(0).toUpperCase() + texto.slice(1);
}
