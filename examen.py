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
COLOR_BG = "#0E1117"         # Fondo oscuro

# CSS AVANZADO: TEXTOS GRANDES Y ALTA LEGIBILIDAD
st.markdown("""
    <style>
    /* Forzar color blanco y tamaño grande en todos los textos */
    html, body, [class*="css"] {
        color: #FFFFFF !important;
        font-family: 'Segoe UI', sans-serif;
    }
    
    h1 {
        color: #4DA6FF !important; /* Azul neón para título principal */
        font-size: 3rem !important;
        font-weight: 800 !important;
        border-bottom: 3px solid #4DA6FF;
        padding-bottom: 15px;
        text-transform: uppercase;
    }
    
    h3 {
        color: #FFD700 !important; /* Dorado para subtítulos */
        font-size: 1.8rem !important;
        font-weight: 600;
        margin-top: 20px;
    }

    /* Caja del Autor */
    .author-box {
        background: linear-gradient(90deg, #1E1E1E 0%, #2D2D2D 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #00B050;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        color: white;
        text-align: right;
        font-size: 1.1rem;
    }

    /* Estilo para los párrafos de teoría (BIG FONT) */
    .theory-text {
        font-size: 1.4rem !important; /* Letra MUY grande */
        line-height: 1.8;
        color: #E0E0E0 !important;
        text-align: justify;
        background-color: rgba(255, 255, 255, 0.05); /* Fondo sutil para leer mejor */
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4DA6FF;
        margin-bottom: 20px;
    }
    
    /* Ajuste de pestañas */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.5rem !important; /* Tamaño de letra en pestañas */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. ENCABEZADO IMPACTANTE
# -----------------------------------------------------------------------------
col1, col2 = st.columns([3, 1.5])
with col1:
    st.title("SISTEMA INTEGRAL DE PLANEACIÓN")
    st.markdown("### 🎯 Enfoque Sistémico: Estrategia, Recursos y Costos")

with col2:
    st.markdown("""
    <div class="author-box">
        <b>Autor:</b> Ing. Jaime Silva Betancourt<br>
        <span style="font-size: 0.9em; color: #AAA;">Maestría en Ingeniería Industrial</span><br>
        <span style="color: #00B050; font-weight: bold;">UO Global University</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------------------------
# 3. ESQUEMA RADIAL GIGANTE
# -----------------------------------------------------------------------------
st.markdown("### 1. Esquema Jerárquico del Sistema (Interactivo)")
st.info("💡 Haz clic en los sectores para hacer ZOOM y explorar la estructura del sistema.")

# Datos de Jerarquía
labels = [
    "SISTEMA<br>INTEGRAL",                
    "ESTRATEGIA", "RECURSOS", "COSTOS",   
    "Plan<br>Agregada", "Estrat.<br>Operaciones", "Objetivos<br>Org.", 
    "Capacidad<br>(CRP)", "Mano de<br>Obra", "Materiales<br>(MRP)",    
    "Mantenimiento<br>(Holding)", "Producción<br>(COGS)", "Faltantes<br>(Riesgo)" 
]

parents = [
    "",                                
    "SISTEMA<br>INTEGRAL", "SISTEMA<br>INTEGRAL", "SISTEMA<br>INTEGRAL", 
    "ESTRATEGIA", "ESTRATEGIA", "ESTRATEGIA",
    "RECURSOS", "RECURSOS", "RECURSOS",
    "COSTOS", "COSTOS", "COSTOS"
]

values = [9, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# Colores (Centro Oscuro para contraste)
colors = [
    "#212F3D",       # Centro OSCURO
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_TERTIARY, 
    "#3498db", "#2980b9", "#1f618d", 
    "#2ecc71", "#27ae60", "#1e8449", 
    "#e74c3c", "#c0392b", "#922b21"
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
        size=24, # Letra GIGANTE en el gráfico
        color="white"
    )
))

fig_map.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),
    height=700, # Gráfico MÁS ALTO
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white")
)

st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# 4. FUNDAMENTACIÓN TEÓRICA (TEXTOS AMPLIADOS Y GRÁFICAS GRANDES)
# -----------------------------------------------------------------------------
st.markdown("### 2. Fundamentación Teórica y Análisis Visual")

tab1, tab2, tab3 = st.tabs(["🟦 ESTRATEGIA (Top-Down)", "🟩 RECURSOS (Restricciones)", "🟥 COSTOS (Optimización)"])

# --- TAB 1: ESTRATEGIA ---
with tab1:
    col1, col2 = st.columns([1, 1.2]) # Columna de gráfico más ancha
    with col1:
        st.markdown("""
        <div class="theory-text">
        <b>El Embudo de la Decisión Estratégica</b><br><br>
        La planeación no es un evento aislado, es una cascada de decisiones. Según <b>Heizer & Render (2020)</b>, la eficiencia en el piso de producción es irrelevante si no está alineada con la <b>Visión Corporativa</b>.<br><br>
        1. <b>Nivel Estratégico:</b> Define el "Qué" (¿Competimos por costo o calidad?).<br>
        2. <b>Nivel Táctico (Plan Agregado):</b> Traduce eso a números mensuales (6-18 meses).<br>
        3. <b>Nivel Operativo (MPS):</b> Detalla el "semana a semana".
        </div>
        """, unsafe_allow_html=True)
    with col2:
        # Funnel Chart
        fig_funnel = go.Figure(go.Funnel(
            y = ["Visión Corporativa", "Estrategia Ops.", "Plan Agregado", "MPS (Semanal)", "Ejecución Diaria"],
            x = [100, 80, 60, 40, 20],
            textinfo = "value+percent initial",
            marker = {"color": [COLOR_PRIMARY, "#1a5276", "#2980b9", "#5499c7", "#a9cce3"]},
            textfont=dict(size=18, color="white")
        ))
        fig_funnel.update_layout(
            title=dict(text="Jerarquía de Planeación Descendente", font=dict(size=24, color="#4DA6FF")),
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            height=500, # ALTURA AUMENTADA
            showlegend=False
        )
        st.plotly_chart(fig_funnel, use_container_width=True)

# --- TAB 2: RECURSOS ---
with tab2:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("""
        <div class="theory-text">
        <b>Gestión de Restricciones (CRP)</b><br><br>
        Un plan perfecto en papel puede fallar en la planta. La gestión de recursos se encarga de validar la <b>Viabilidad Física</b>.<br><br>
        El gráfico adjunto simula un análisis de <b>Carga vs. Capacidad</b>. Observe la <b>Semana 2</b>: La barra verde (Demanda) supera la línea roja (Capacidad Máxima).<br>
        Esto activa una alerta gerencial: ¿Autorizamos horas extra o subcontratamos? Sin este análisis, el resultado sería un pedido retrasado.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        # Bar Chart con Anotaciones
        fig_res = go.Figure()
        fig_res.add_trace(go.Bar(x=['Sem 1', 'Sem 2', 'Sem 3'], y=[850, 1250, 900], name='Carga Requerida', marker_color=COLOR_SECONDARY))
        fig_res.add_trace(go.Scatter(x=['Sem 1', 'Sem 2', 'Sem 3'], y=[1000, 1000, 1000], name='Capacidad Máxima', line=dict(color='red', width=5, dash='dash')))
        
        # Añadir flecha de alerta
        fig_res.add_annotation(x='Sem 2', y=1250, text="¡SOBRECARGA!", showarrow=True, arrowhead=1, ax=0, ay=-40, font=dict(color="red", size=20, family="Arial Black"))

        fig_res.update_layout(
            title=dict(text="Análisis de Capacidad (Cuellos de Botella)", font=dict(size=24, color="#00B050")),
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(255,255,255,0.05)', 
            font=dict(color="white", size=16),
            height=500 # ALTURA AUMENTADA
        )
        st.plotly_chart(fig_res, use_container_width=True)

# --- TAB 3: COSTOS ---
with tab3:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("""
        <div class="theory-text">
        <b>Optimización del Costo Total</b><br><br>
        El objetivo no es "cero inventario", sino el <b>Mínimo Costo Total</b>. Existe un <i>Trade-off</i> invisible:<br><br>
        * <b>Costos Visibles:</b> Materia prima y Mano de obra (COGS).<br>
        * <b>Costos Ocultos (Iceberg):</b> El costo de mantener stock (H) y, peor aún, el costo de <b>Faltantes (Stockout)</b>.<br><br>
        Como muestra el gráfico, reducir demasiado el inventario (área roja) puede disparar los costos por ventas perdidas (área rosa).
        </div>
        """, unsafe_allow_html=True)
    with col2:
        # Pie Chart
        fig_cost = go.Figure(data=[go.Pie(
            labels=['Producción (COGS)', 'Almacenaje (H)', 'Faltantes (Riesgo)', 'Admin'], 
            values=[50, 25, 15, 10], 
            hole=.4,
            textinfo='label+percent',
            textfont=dict(size=16)
        )])
        fig_cost.update_layout(
            title=dict(text="Estructura de Costos Logísticos", font=dict(size=24, color="#C00000")),
            paper_bgcolor='rgba(0,0,0,0)', 
            font=dict(color="white"),
            height=500 # ALTURA AUMENTADA
        )
        st.plotly_chart(fig_cost, use_container_width=True)

st.markdown("---")
with st.expander("📚 Referencias Bibliográficas (APA 7.0)"):
    st.markdown("""
    <div style="font-size: 1.2rem; color: #BBB;">
    * Heizer, J., Render, B., & Munson, C. (2020). <i>Principios de administración de operaciones: Sostenibilidad y gestión de la cadena de suministro</i>. Pearson.<br>
    * Chase, R. B., & Jacobs, F. R. (2018). <i>Administración de operaciones: Producción y cadena de suministros</i>. McGraw-Hill Education.<br>
    * Chopra, S., & Meindl, P. (2016). <i>Administración de la cadena de suministro</i>. Pearson Educación.
    </div>
    """, unsafe_allow_html=True)
