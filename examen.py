import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Sistema de Planeación - Ing. Silva")

# Definición de Colores Corporativos
COLOR_PRIMARY = "#003366"    # Azul Estrategia
COLOR_SECONDARY = "#00B050"  # Verde Recursos
COLOR_TERTIARY = "#C00000"   # Rojo Costos
COLOR_BG = "#0E1117"         # Fondo oscuro compatible con Streamlit

# CSS para forzar textos claros y legibles
st.markdown("""
    <style>
    h1 {
        color: #4DA6FF !important;
        border-bottom: 2px solid #4DA6FF;
        padding-bottom: 10px;
    }
    h2, h3, p, li {
        color: #E0E0E0 !important;
    }
    .author-box {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        border-right: 5px solid #00B050;
        color: white;
        text-align: right;
    }
    .big-font {
        font-size: 1.15rem;
        line-height: 1.6;
        text-align: justify;
        color: #E0E0E0;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. ENCABEZADO
# -----------------------------------------------------------------------------
col1, col2 = st.columns([3, 1])
with col1:
    st.title("SISTEMA INTEGRAL DE PLANEACIÓN")
    st.markdown("### Enfoque Sistémico: Estrategia, Recursos y Costos")

with col2:
    st.markdown("""
    <div class="author-box">
        <b>Autor:</b> Ing. Jaime Silva Betancourt<br>
        <b>Maestría en Ingeniería Industrial</b><br>
        UO Global University
    </div>
    """, unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------------------------
# 3. ESQUEMA RADIAL (CORREGIDO: CENTRO OSCURO)
# -----------------------------------------------------------------------------
st.subheader("1. Esquema Jerárquico del Sistema (Interactivo)")
st.info("💡 Haz clic en los sectores para hacer zoom. El esquema muestra la integración de los 3 pilares.")

# Datos de Jerarquía
labels = [
    "SISTEMA<br>INTEGRAL",                # Centro
    "ESTRATEGIA", "RECURSOS", "COSTOS",   # Nivel 1
    "Plan<br>Agregada", "Estrat.<br>Operaciones", "Objetivos<br>Org.", # Nivel 2
    "Capacidad<br>(CRP)", "Mano de<br>Obra", "Materiales<br>(MRP)",    # Nivel 2
    "Mantenimiento<br>(Holding)", "Producción<br>(COGS)", "Faltantes<br>(Riesgo)" # Nivel 2
]

parents = [
    "",                                
    "SISTEMA<br>INTEGRAL", "SISTEMA<br>INTEGRAL", "SISTEMA<br>INTEGRAL", 
    "ESTRATEGIA", "ESTRATEGIA", "ESTRATEGIA",
    "RECURSOS", "RECURSOS", "RECURSOS",
    "COSTOS", "COSTOS", "COSTOS"
]

values = [9, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# --- CORRECCIÓN DE COLOR AQUÍ ---
# Cambiamos el primer color (Centro) de gris claro a #2c3e50 (Gris Oscuro/Azulino)
colors = [
    "#2c3e50",       # <--- AHORA ES OSCURO PARA QUE SE LEA EL TEXTO BLANCO
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_TERTIARY, 
    "#3498db", "#3498db", "#3498db", 
    "#2ecc71", "#2ecc71", "#2ecc71", 
    "#e74c3c", "#e74c3c", "#e74c3c"
]

hovers = [
    "Visión Holística",
    "Alineación Top-Down", "Gestión de Entradas (4M)", "Control Financiero",
    "Equilibrio Oferta/Demanda (6-18 meses)", "Ventaja Competitiva", "KPIs: ROI, Nivel de Servicio",
    "Restricciones y Cuellos de Botella", "Gestión del Talento Humano", "Gestión de Stock y BOM",
    "Costo de oportunidad y obsolescencia", "Materia Prima y Mano de Obra", "Riesgo de Stockout"
]

fig_map = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",
    marker=dict(colors=colors),
    hovertext=hovers,
    hoverinfo="label+text",
    insidetextorientation='auto', 
    textfont=dict(
        family="Arial Black",
        size=18,
        color="white" # Texto blanco
    )
))

fig_map.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),
    height=600,
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white")
)

st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# 4. PANELES DE ANÁLISIS
# -----------------------------------------------------------------------------
st.subheader("2. Fundamentación Teórica")

tab1, tab2, tab3 = st.tabs(["🟦 Estrategia", "🟩 Recursos", "🟥 Costos"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="big-font">
        <b>1. Elementos Estratégicos:</b><br>
        La planeación agregada actúa como el puente entre la estrategia corporativa y la ejecución. 
        Se enfoca en equilibrar la oferta y la demanda en el mediano plazo (6-18 meses).
        </div>
        """, unsafe_allow_html=True)
    with col2:
        fig_funnel = go.Figure(go.Funnel(
            y = ["Visión", "Estrategia", "Plan Agregado", "MPS"],
            x = [100, 80, 60, 40],
            textinfo = "value+percent initial",
            marker = {"color": [COLOR_PRIMARY, "#1f618d", "#2980b9", "#5499c7"]},
            textfont=dict(color="white")
        ))
        fig_funnel.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), showlegend=False, height=300)
        st.plotly_chart(fig_funnel, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="big-font">
        <b>2. Gestión de Recursos:</b><br>
        Determina la viabilidad física del plan. El análisis CRP (Capacity Requirements Planning) 
        es vital para detectar cuellos de botella antes de liberar órdenes al piso.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        fig_res = go.Figure()
        fig_res.add_trace(go.Bar(x=['S1', 'S2', 'S3'], y=[850, 1200, 900], name='Carga', marker_color=COLOR_SECONDARY))
        fig_res.add_trace(go.Scatter(x=['S1', 'S2', 'S3'], y=[1000, 1000, 1000], name='Límite', line=dict(color='red', width=3, dash='dash')))
        fig_res.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=300)
        st.plotly_chart(fig_res, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="big-font">
        <b>3. Costos y Gastos:</b><br>
        El sistema busca el óptimo global, minimizando la suma de Costos de Producción + 
        Costos de Inventario (H) + Costos de Faltantes (Riesgo).
        </div>
        """, unsafe_allow_html=True)
    with col2:
        fig_cost = go.Figure(data=[go.Pie(labels=['Prod.', 'Holding', 'Faltantes'], values=[50, 30, 20], hole=.4)])
        fig_cost.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=300)
        st.plotly_chart(fig_cost, use_container_width=True)

st.markdown("---")
with st.expander("📚 Referencias Bibliográficas (APA 7.0)"):
    st.markdown("""
    * Heizer, J., Render, B., & Munson, C. (2020). *Principios de administración de operaciones*. Pearson.
    * Chase, R., & Jacobs, F. (2018). *Administración de operaciones*. McGraw-Hill.
    """)
