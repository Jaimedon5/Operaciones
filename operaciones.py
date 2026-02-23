import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILO
# -----------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Sistema de Planeación - Ing. Silva")

# Definición de Colores Corporativos
COLOR_PRIMARY = "#003366"  # Azul Estrategia
COLOR_SECONDARY = "#00B050" # Verde Recursos
COLOR_TERTIARY = "#C00000"  # Rojo Costos
COLOR_BG = "#0b1220"

# CSS Personalizado para dar formato académico
st.markdown(f"""
    <style>
    :root {{
        --bg: {COLOR_BG};
        --panel: #111827;
        --panel-2: #0f172a;
        --text: #e5e7eb;
        --muted: #9ca3af;
        --accent: {COLOR_PRIMARY};
        --gold: #c9a65d;
        --border: rgba(201, 166, 93, 0.6);
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        background: radial-gradient(1200px 600px at 15% 0%, #0f172a, #0b1220 60%) !important;
        color: var(--text) !important;
        font-family: 'Arial', sans-serif;
    }}

    .main, .block-container {{
        background-color: transparent !important;
    }}

    h1, h2, h3, h4, h5 {{
        color: var(--text) !important;
        font-family: 'Arial Black', 'Arial', sans-serif;
        letter-spacing: 0.3px;
    }}

    h1 {{
        border-bottom: 2px solid var(--accent);
        padding-bottom: 10px;
    }}

    p, li, span, label {{
        color: var(--text) !important;
    }}

    .author-card {{
        background: linear-gradient(180deg, #0f1b33 0%, #0b1528 100%);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 12px 14px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
    }}

    .author-tag {{
        font-size: 1.05rem;
        color: var(--gold);
        font-weight: bold;
        text-align: right;
        letter-spacing: 0.2px;
    }}

    .author-subtitle {{
        color: #9cc5ff;
        font-size: 0.95rem;
        text-align: right;
        margin-top: 6px;
    }}

    .subtitle-accent {{
        color: #9cc5ff;
        font-weight: 600;
    }}

    .citation {{
        font-size: 0.8rem;
        color: var(--muted);
        font-style: italic;
    }}

    .big-font {{
        font-size: 1.05rem;
        line-height: 1.7;
        text-align: justify;
        color: var(--text);
    }}

    .stMarkdown, .stCaption {{
        color: var(--text) !important;
    }}

    [data-testid="stMetric"] {{
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 10px 12px;
    }}

    [data-testid="stExpander"] {{
        background: var(--panel-2);
        border: 1px solid var(--border);
        border-radius: 12px;
    }}

    .stPlotlyChart {{
        background: var(--panel-2);
        border-radius: 14px;
        padding: 8px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }}

    hr, .stDivider {{
        border-color: rgba(255, 255, 255, 0.12) !important;
    }}
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# ENCABEZADO ACADÉMICO
# -----------------------------------------------------------------------------
col_header_1, col_header_2 = st.columns([3, 1])
with col_header_1:
    st.title("SISTEMA INTEGRAL DE PLANEACIÓN DE LA PRODUCCIÓN")
    st.markdown('<span class="subtitle-accent">Enfoque Sistémico: Estrategia, Recursos y Costos</span>', unsafe_allow_html=True)

with col_header_2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="author-card">'
        '<div class="author-tag">Autor:<br>Ing. Jaime Silva Betancourt</div>'
        '<div class="author-subtitle">Maestría en Ingeniería Industrial</div>'
        '</div>',
        unsafe_allow_html=True
    )

st.divider()
# -----------------------------------------------------------------------------
# MENÚ LATERAL
# -----------------------------------------------------------------------------
st.sidebar.title("Menu")
section = st.sidebar.radio(
    "Navegacion",
    ["Portada", "Semana 1", "Semana 2", "Semana 3", "Semana 4"],
    index=0
)

if section == "Portada":
    st.markdown("### Portada")
    st.markdown(
        """
        Bienvenido al sistema integral de planeacion de la produccion.
        Use el menu lateral para navegar por las semanas del curso.
        """
    )

elif section == "Semana 1":
    st.markdown("### Semana 1: Linea de tiempo")
    st.markdown("Haga clic en los nodos circulares para desplegar el analisis detallado.")

    html_path = Path(__file__).parent / "assets" / "semana_1_timeline.html"
    if html_path.exists():
        timeline_html = html_path.read_text(encoding="utf-8", errors="ignore")
        components.html(timeline_html, height=900, scrolling=True)
    else:
        st.error("No se encontro el archivo de linea de tiempo. Verifique la carpeta assets.")

elif section == "Semana 2":
    st.markdown("### Semana 2")
    st.info("Contenido en construccion. Indique que se debe incluir aqui.")

elif section == "Semana 3":
    st.markdown("""
    ### Objetivo de la actividad
    Elabora un esquema o mapa conceptual (o mapa mental) en el que representes el Sistema de Planeacion de la Produccion, destacando de manera clara principales elementos que se debe considerar:

    - La integracion de los elementos estrategicos (planeacion agregada, estrategia de operaciones, objetivos organizacionales).
    - Los elementos relacionados con la gestion de recursos (capacidad, mano de obra, materiales).
    - Los aspectos vinculados a costos y gastos dentro del sistema de planeacion.
    - Incluye palabras clave o breves descripciones que expliquen la funcion de cada elemento dentro del sistema.
    """)

    st.subheader("1. Mapa Conceptual Jerarquico del Sistema")
    st.markdown("""
    Este diagrama interactivo presenta la jerarquia del sistema en formato tipo pastel.
    Haga clic en cada seccion para desplegar los niveles inferiores y explorar la relacion entre decisiones.
    """)

    labels = [
        "SISTEMA DE PLANEACION DE LA PRODUCCION",
        "ELEMENTOS ESTRATEGICOS",
        "GESTION DE RECURSOS",
        "COSTOS Y GASTOS",
        "Planeacion Agregada (6-18 meses)",
        "Programa Maestro (MPS)",
        "Estrategia de Operaciones",
        "Objetivos Organizacionales (ROI, Share)",
        "Capacidad (Instalaciones)",
        "Mano de Obra (Fuerza Laboral)",
        "Materiales (MRP / BOM)",
        "Costos de Inventario",
        "Costos de Produccion",
        "Costos de Faltantes"
    ]

    parents = [
        "",
        "SISTEMA DE PLANEACION DE LA PRODUCCION",
        "SISTEMA DE PLANEACION DE LA PRODUCCION",
        "SISTEMA DE PLANEACION DE LA PRODUCCION",
        "ELEMENTOS ESTRATEGICOS",
        "ELEMENTOS ESTRATEGICOS",
        "ELEMENTOS ESTRATEGICOS",
        "ELEMENTOS ESTRATEGICOS",
        "GESTION DE RECURSOS",
        "GESTION DE RECURSOS",
        "GESTION DE RECURSOS",
        "COSTOS Y GASTOS",
        "COSTOS Y GASTOS",
        "COSTOS Y GASTOS"
    ]

    values = [100, 35, 35, 30, 10, 8, 9, 8, 12, 12, 11, 10, 10, 10]

    colors = [
        "#2c3e50",
        COLOR_PRIMARY,
        COLOR_SECONDARY,
        COLOR_TERTIARY,
        "#d6e6f2",
        "#d6e6f2",
        "#d6e6f2",
        "#d6e6f2",
        "#d9f2e3",
        "#d9f2e3",
        "#d9f2e3",
        "#f5d6d6",
        "#f5d6d6",
        "#f5d6d6"
    ]

    fig_sunburst = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        marker=dict(colors=colors, line=dict(color="#ffffff", width=2)),
        insidetextorientation="radial",
        hovertemplate="%{label}<extra></extra>",
        maxdepth=2
    ))

    fig_sunburst.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        height=600
    )

    st.plotly_chart(fig_sunburst, use_container_width=True)

    st.divider()

    st.subheader("2. Desglose Analitico y Visualizacion de Datos")
    st.markdown("Analisis profundo de los tres pilares fundamentales, sustentado en teoria de operaciones.")

    # --- ESTRATEGIA ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Alineacion Estrategica (Top-Down)")
        st.markdown("""
        <div class="big-font">
        La planeacion de la produccion no es un evento aislado, sino la traduccion operativa de la vision empresarial.
        Segun <b>Heizer y Render (2020)</b>, la estrategia de operaciones debe alinearse con la mision para generar una ventaja competitiva sostenible.
        
        * <b>Planeacion Agregada:</b> Equilibra la oferta y demanda a mediano plazo, definiendo niveles de produccion, inventario y mano de obra.
        * <b>Objetivos Organizacionales:</b> Se traducen en KPIs como Nivel de Servicio y Rotacion de Activos.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        fig_strat = go.Figure(go.Funnel(
            y = ["Vision Corporativa", "Estrategia Operaciones", "Planeacion Agregada", "Programa Maestro (MPS)", "Ejecucion (Piso)"],
            x = [100, 80, 60, 40, 20],
            textinfo = "value+percent initial",
            marker = {"color": [COLOR_PRIMARY, "#1a5276", "#2980b9", "#5499c7", "#a9cce3"]}
        ))
        fig_strat.update_layout(title="Jerarquia de la Planeacion (Despliegue)", showlegend=False, height=350)
        st.plotly_chart(fig_strat, use_container_width=True)
        st.caption("Fig 1. El 'Embudo de Decision': Como la estrategia se refina hasta llegar a la orden de produccion.")

    st.divider()

    # --- RECURSOS ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Gestion de la Capacidad y Materiales")
        st.markdown("""
        <div class="big-font">
        La gestion de recursos busca asegurar la disponibilidad de los factores de produccion (4M: Materiales, Maquinas, Mano de obra, Metodos).
        
        * <b>Capacidad:</b> Determina el "techo" de produccion. Segun <b>Chase y Jacobs (2018)</b>, la planeacion debe considerar la eficiencia (OEE) y no solo la capacidad teorica.
        * <b>Materiales (MRP):</b> Transforma los requerimientos brutos en netos mediante la Lista de Materiales (BOM) y el inventario disponible.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        categories = ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4']
        capacity = [1000, 1000, 1000, 1000]
        load = [850, 920, 1150, 780]

        fig_res = go.Figure()
        fig_res.add_trace(go.Bar(x=categories, y=load, name='Carga Requerida (Demanda)', marker_color=COLOR_SECONDARY))
        fig_res.add_trace(go.Scatter(x=categories, y=capacity, mode='lines', name='Capacidad Disponible', line=dict(color='red', width=3, dash='dash')))
        
        fig_res.update_layout(title="Analisis CRP (Capacity Requirements Planning)", height=350)
        st.plotly_chart(fig_res, use_container_width=True)
        st.caption("Fig 2. Visualizacion de cuellos de botella: La Semana 3 excede la capacidad instalada, requiriendo horas extra.")

    st.divider()

    # --- COSTOS ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Estructura de Costos y Optimizacion")
        st.markdown("""
        <div class="big-font">
        El objetivo final es minimizar el Costo Total Relevante. Existe un <i>Trade-off</i> constante entre nivel de servicio e inventario.
        
        * <b>Costos de Inventario (H):</b> Incluyen capital inmovilizado, seguros y obsolescencia. Representan entre el 15-40% del valor del producto al ano.
        * <b>Costo de Faltantes:</b> Es el mas critico y dificil de medir (perdida de clientes y reputacion).
        </div>
        """, unsafe_allow_html=True)

    with col2:
        labels_cost = ['Materia Prima', 'Mano de Obra', 'Mantenimiento Inv (H)', 'Costos de Pedir (S)', 'Faltantes']
        values_cost = [45, 25, 15, 10, 5]
        colors_cost = [COLOR_TERTIARY, '#e74c3c', '#ec7063', '#f1948a', '#fadbd8']

        fig_cost = go.Figure(data=[go.Pie(labels=labels_cost, values=values_cost, hole=.4, marker_colors=colors_cost)])
        fig_cost.update_layout(title="Distribucion Tipica del Costo Logistico", height=350)
        st.plotly_chart(fig_cost, use_container_width=True)
        st.caption("Fig 3. El costo de mantenimiento (H) es un costo oculto significativo que la planeacion busca reducir.")

    st.divider()

    with st.expander("Referencias Bibliograficas (Formato APA 7.0)", expanded=True):
        st.markdown("""
        * Chase, R. B., & Jacobs, F. R. (2018). *Administracion de operaciones: Produccion y cadena de suministros* (15.ª ed.). McGraw-Hill Education.
        * Chopra, S., & Meindl, P. (2016). *Administracion de la cadena de suministro: Estrategia, planeacion y operacion* (6.ª ed.). Pearson Educacion.
        * Heizer, J., Render, B., & Munson, C. (2020). *Principios de administracion de operaciones* (13.ª ed.). Pearson.
        * Krajewski, L. J., Malhotra, M. K., & Ritzman, L. P. (2019). *Administracion de operaciones: Procesos y cadenas de valor* (12.ª ed.). Pearson.
        """)

elif section == "Semana 4":
    st.markdown("### Semana 4")
    st.info("Contenido en construccion. Indique que se debe incluir aqui.")

# Footer simple
st.markdown("---")
st.markdown("*Generado para la asignatura de Planeación y Control de la Producción | Maestría en Ingeniería*")
