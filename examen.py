import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILO
# -----------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Sistema de Planeación - Ing. Silva")

# Definición de Colores Corporativos
COLOR_PRIMARY = "#003366"  # Azul Estrategia
COLOR_SECONDARY = "#00B050" # Verde Recursos
COLOR_TERTIARY = "#C00000"  # Rojo Costos
COLOR_BG = "#F0F2F6"

# CSS Personalizado para dar formato académico
st.markdown(f"""
    <style>
    .main {{
        background-color: {COLOR_BG};
    }}
    h1 {{
        color: {COLOR_PRIMARY};
        font-family: 'Helvetica Neue', sans-serif;
        border-bottom: 2px solid {COLOR_PRIMARY};
        padding-bottom: 10px;
    }}
    h2, h3 {{
        color: #333;
    }}
    .author-tag {{
        font-size: 1.2rem;
        color: #555;
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
# ENCABEZADO ACADÉMICO
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
# 1. MAPA CONCEPTUAL INTERACTIVO (SUNBURST - SIN GRAPHVIZ)
# -----------------------------------------------------------------------------
st.subheader("1. Mapa Conceptual Jerárquico del Sistema")
st.info("💡 Instrucción: Haz clic en los sectores del gráfico para 'entrar' y ver los detalles de cada rama. Haz clic en el centro para volver a salir.")

# Datos Estructurados para el Gráfico
df_map = pd.DataFrame({
    'id': ['Sistema', 'Estratégico', 'Recursos', 'Costos', 
           'Plan Agregada', 'Estrat. Operaciones', 'Objetivos Org.',
           'Capacidad (OEE)', 'Mano de Obra', 'Materiales (BOM)',
           'Mantenimiento (H)', 'Producción (COGS)', 'Faltantes'],
    'parent': ['', 'Sistema', 'Sistema', 'Sistema', 
               'Estratégico', 'Estratégico', 'Estratégico',
               'Recursos', 'Recursos', 'Recursos',
               'Costos', 'Costos', 'Costos'],
    'valor': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'desc': ['Visión Integral', 'Nivel Táctico', 'Factores 4M', 'Control Financiero',
             '6-18 Meses', 'Ventaja Competitiva', 'KPIs',
             'Restricciones', 'Talento Humano', 'MRP',
             'Obsolescencia', 'Materia Prima', 'Riesgo Stockout']
})

# Creación del Gráfico Sunburst
fig_map = px.sunburst(
    df_map, ids='id', parents='parent', values='valor',
    color='id', 
    color_discrete_map={
        'Sistema': '#2c3e50', 'Estratégico': COLOR_PRIMARY, 'Recursos': COLOR_SECONDARY, 'Costos': COLOR_TERTIARY,
        'Plan Agregada': '#2980b9', 'Capacidad (OEE)': '#27ae60', 'Mantenimiento (H)': '#c0392b'
    },
    hover_data=['desc']
)
fig_map.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=600)

st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# 2. ANÁLISIS VISUAL Y TEÓRICO (TABS)
# -----------------------------------------------------------------------------
st.subheader("2. Desglose Analítico y Visualización de Datos")
st.markdown("Análisis profundo de los tres pilares fundamentales, sustentado en teoría de operaciones.")

tab1, tab2, tab3 = st.tabs(["🟦 I. Elementos Estratégicos", "🟩 II. Gestión de Recursos", "🟥 III. Costos y Gastos"])

# --- TAB 1: ESTRATEGIA ---
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Alineación Estratégica (Top-Down)")
        st.markdown("""
        <div class="big-font">
        La planeación de la producción no es un evento aislado, sino la traducción operativa de la visión empresarial.
        Según <b>Heizer y Render (2020)</b>, la estrategia de operaciones debe alinearse con la misión para generar una ventaja competitiva sostenible.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        fig_strat = go.Figure(go.Funnel(
            y = ["Visión Corporativa", "Estrategia Operaciones", "Planeación Agregada", "Programa Maestro (MPS)"],
            x = [100, 80, 60, 40],
            textinfo = "value+percent initial",
            marker = {"color": [COLOR_PRIMARY, "#1a5276", "#2980b9", "#5499c7"]}
        ))
        fig_strat.update_layout(title="Jerarquía de la Planeación (Despliegue)", showlegend=False, height=300)
        st.plotly_chart(fig_strat, use_container_width=True)

# --- TAB 2: RECURSOS ---
with tab2:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Gestión de la Capacidad y Materiales")
        st.markdown("""
        <div class="big-font">
        La gestión de recursos busca asegurar la disponibilidad de los factores de producción (4M).
        <b>Chase y Jacobs (2018)</b> enfatizan que la planeación debe considerar la eficiencia (OEE) y no solo la capacidad teórica.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        fig_res = go.Figure()
        fig_res.add_trace(go.Bar(x=['Sem 1', 'Sem 2', 'Sem 3'], y=[850, 1150, 950], name='Carga', marker_color=COLOR_SECONDARY))
        fig_res.add_trace(go.Scatter(x=['Sem 1', 'Sem 2', 'Sem 3'], y=[1000, 1000, 1000], name='Capacidad Max', line=dict(color='red', width=3, dash='dash')))
        fig_res.update_layout(title="Análisis CRP (Carga vs Capacidad)", height=300)
        st.plotly_chart(fig_res, use_container_width=True)

# --- TAB 3: COSTOS ---
with tab3:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Estructura de Costos y Optimización")
        st.markdown("""
        <div class="big-font">
        El objetivo final es minimizar el Costo Total Relevante. Existe un <i>Trade-off</i> constante entre nivel de servicio e inventario (Stockout vs Holding Cost).
        </div>
        """, unsafe_allow_html=True)
    with col2:
        fig_cost = go.Figure(data=[go.Pie(labels=['Materiales', 'Mano de Obra', 'Holding (H)', 'Faltantes'], values=[45, 25, 20, 10], hole=.4)])
        fig_cost.update_layout(title="Distribución del Costo Logístico", height=300)
        st.plotly_chart(fig_cost, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# REFERENCIAS BIBLIOGRÁFICAS (APA 7.0)
# -----------------------------------------------------------------------------
with st.expander("📚 Referencias Bibliográficas (Formato APA 7.0)", expanded=True):
    st.markdown("""
    * Chase, R. B., & Jacobs, F. R. (2018). *Administración de operaciones: Producción y cadena de suministros* (15.ª ed.). McGraw-Hill Education.
    * Chopra, S., & Meindl, P. (2016). *Administración de la cadena de suministro: Estrategia, planeación y operación* (6.ª ed.). Pearson Educación.
    * Heizer, J., Render, B., & Munson, C. (2020). *Principios de administración de operaciones* (13.ª ed.). Pearson.
    """)

st.markdown("---")
st.markdown("*Generado para la asignatura de Planeación y Control de la Producción | Maestría en Ingeniería*")
