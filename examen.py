import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero)
# -----------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Sistema de Planeación - Ing. Silva")

# Definición de Colores de Alto Contraste
COLOR_PRIMARY = "#003366"    # Azul Oscuro
COLOR_SECONDARY = "#00B050"  # Verde Intenso
COLOR_TERTIARY = "#C00000"   # Rojo Intenso

# CSS Ajustado: Eliminamos el background fijo para evitar conflictos con Modo Oscuro
st.markdown(f"""
    <style>
    h1 {{
        color: {COLOR_PRIMARY};
        font-family: 'Helvetica Neue', sans-serif;
        border-bottom: 2px solid {COLOR_PRIMARY};
        padding-bottom: 10px;
    }}
    .author-tag {{
        font-size: 1.2rem;
        color: #888;
        font-weight: bold;
        text-align: right;
    }}
    .big-font {{
        font-size: 1.1rem;
        line-height: 1.6;
        text-align: justify;
    }}
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. ENCABEZADO
# -----------------------------------------------------------------------------
col_header_1, col_header_2 = st.columns([3, 1])
with col_header_1:
    st.title("SISTEMA INTEGRAL DE PLANEACIÓN DE LA PRODUCCIÓN")
    st.markdown("**Enfoque Sistémico: Estrategia, Recursos y Costos**")

with col_header_2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="author-tag">Autor:<br>Ing. Jaime Silva Betancourt</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: right;">Maestría en Ingeniería Industrial</div>', unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------------------------
# 3. MAPA CONCEPTUAL (CORREGIDO - Graph Objects)
# -----------------------------------------------------------------------------
st.subheader("1. Mapa Conceptual Jerárquico del Sistema")
st.info("💡 Instrucción: Haz clic en los sectores del gráfico para 'entrar'. Haz clic en el centro para regresar.")

# Definición manual de la jerarquía para asegurar que no falle el renderizado
# Estructura: Raíz -> 3 Ramas -> 3 Hojas cada una
labels = [
    "SISTEMA INTEGRAL",                # Raíz
    "ESTRATEGIA", "RECURSOS", "COSTOS", # Nivel 1
    "Plan Agregada", "Estrat. Operaciones", "Objetivos Org.", # Hojas de Estrategia
    "Capacidad (CRP)", "Mano de Obra", "Materiales (MRP)",    # Hojas de Recursos
    "Mantenimiento (H)", "Producción", "Faltantes (Riesgo)"   # Hojas de Costos
]

parents = [
    "",                                # Raíz no tiene padre
    "SISTEMA INTEGRAL", "SISTEMA INTEGRAL", "SISTEMA INTEGRAL", # Padres Nivel 1
    "ESTRATEGIA", "ESTRATEGIA", "ESTRATEGIA",
    "RECURSOS", "RECURSOS", "RECURSOS",
    "COSTOS", "COSTOS", "COSTOS"
]

# Valores matemáticamente consistentes (Hojas=1, Ramas=3, Raíz=9)
values = [
    9,          # Raíz (3+3+3)
    3, 3, 3,    # Ramas
    1, 1, 1,    # Hojas Estrategia
    1, 1, 1,    # Hojas Recursos
    1, 1, 1     # Hojas Costos
]

colors = [
    "#2c3e50",  # Raíz (Gris oscuro)
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_TERTIARY, # Ramas
    "#3498db", "#3498db", "#3498db", # Azules claros
    "#2ecc71", "#2ecc71", "#2ecc71", # Verdes claros
    "#e74c3c", "#e74c3c", "#e74c3c"  # Rojos claros
]

# Creación del Gráfico Robusto
fig_map = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total", # Fuerza a que la matemática sea exacta
    marker=dict(colors=colors),
    hovertemplate='<b>%{label}</b><br>Peso en el sistema: %{value}<extra></extra>',
    insidetextorientation='radial'
))

fig_map.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),
    height=600,
    paper_bgcolor='rgba(0,0,0,0)' # Fondo transparente para que funcione en Dark Mode
)

st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# 4. ANÁLISIS VISUAL (TABS)
# -----------------------------------------------------------------------------
st.subheader("2. Desglose Analítico y Visualización de Datos")

tab1, tab2, tab3 = st.tabs(["🟦 I. Elementos Estratégicos", "🟩 II. Gestión de Recursos", "🟥 III. Costos y Gastos"])

# --- TAB 1: ESTRATEGIA ---
with tab1:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### Alineación Estratégica (Top-Down)")
        st.markdown("""
        <div class="big-font">
        La estrategia desciende desde la alta dirección hasta el piso de producción.
        <b>Heizer y Render (2020)</b> establecen que sin una alineación clara, la eficiencia operativa carece de rumbo.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        fig_funnel = go.Figure(go.Funnel(
            y = ["1. Visión Corporativa", "2. Estrategia Ops.", "3. Plan Agregado", "4. Plan Maestro (MPS)"],
            x = [100, 80, 60, 40],
            textinfo = "value+percent initial",
            marker = {"color": [COLOR_PRIMARY, "#154360", "#1A5276", "#2980B9"]}
        ))
        fig_funnel.update_layout(title="Embudo de Decisión", showlegend=False, height=300)
        st.plotly_chart(fig_funnel, use_container_width=True)

# --- TAB 2: RECURSOS ---
with tab2:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### Balance de Capacidad (CRP)")
        st.markdown("""
        <div class="big-font">
        La gestión de recursos valida la viabilidad del plan.
        El gráfico muestra un <b>Cuello de Botella en la Semana 3</b>, donde la demanda supera la capacidad instalada.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        fig_res = go.Figure()
        fig_res.add_trace(go.Bar(x=['S1', 'S2', 'S3', 'S4'], y=[850, 950, 1150, 900], name='Carga', marker_color=COLOR_SECONDARY))
        fig_res.add_trace(go.Scatter(x=['S1', 'S2', 'S3', 'S4'], y=[1000, 1000, 1000, 1000], name='Capacidad Max', line=dict(color='red', width=3, dash='dash')))
        fig_res.update_layout(title="Análisis Carga vs Capacidad", height=300)
        st.plotly_chart(fig_res, use_container_width=True)

# --- TAB 3: COSTOS ---
with tab3:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### El Iceberg de los Costos")
        st.markdown("""
        <div class="big-font">
        El costo visible (Producción) es solo una parte. Los costos ocultos como el <b>Mantenimiento de Inventario (H)</b> y los Faltantes impactan gravemente la utilidad.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        fig_pie = go.Figure(data=[go.Pie(labels=['Producción', 'Holding (H)', 'Faltantes', 'Admin'], values=[50, 25, 15, 10], hole=.4)])
        fig_pie.update_layout(title="Estructura de Costos Logísticos", height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")
with st.expander("📚 Referencias Bibliográficas"):
    st.markdown("""
    * Chase, R. B., & Jacobs, F. R. (2018). *Administración de operaciones*. McGraw-Hill.
    * Heizer, J., & Render, B. (2020). *Principios de administración de operaciones*. Pearson.
    """)
