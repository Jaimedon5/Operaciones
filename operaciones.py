import streamlit as st
import graphviz
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
    .citation {{
        font-size: 0.8rem;
        color: #666;
        font-style: italic;
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
# 1. MAPA CONCEPTUAL (GRAPHVIZ)
# -----------------------------------------------------------------------------
st.subheader("1. Mapa Conceptual Jerárquico del Sistema")
st.markdown("""
Este diagrama representa la interconexión lógica entre los niveles de decisión. 
Se observa cómo la estrategia *descendente* (Top-Down) condiciona los recursos y cómo los costos actúan como restricción de control.
""")

# Crear el grafo
dot = graphviz.Digraph(comment='Sistema de Planeación')
dot.attr(rankdir='TB', size='10')  # Top to Bottom

# Nodos Principales
dot.attr('node', shape='box', style='filled', fontname='Helvetica', fontcolor='white')

# Nodo Central
dot.node('CENTER', 'SISTEMA DE\nPLANEACIÓN', fillcolor='#2c3e50', fontsize='16')

# Ramas
dot.node('EST', 'ELEMENTOS\nESTRATÉGICOS', fillcolor=COLOR_PRIMARY)
dot.node('REC', 'GESTIÓN DE\nRECURSOS', fillcolor=COLOR_SECONDARY)
dot.node('COS', 'COSTOS Y\nGASTOS', fillcolor=COLOR_TERTIARY)

# Hojas (Detalles) - Estilo diferente
dot.attr('node', shape='ellipse', style='filled', fontcolor='black', fillcolor='white', color='black')

# Estrategia
dot.edge('CENTER', 'EST', penwidth='2')
dot.edge('EST', 'PA', label='Nivel Táctico')
dot.node('PA', 'Planeación\nAgregada\n(6-18 meses)')
dot.edge('EST', 'EO', label='Ventaja Comp.')
dot.node('EO', 'Estrategia de\nOperaciones')
dot.edge('EST', 'OBJ', label='Metas')
dot.node('OBJ', 'Objetivos\nOrganizacionales\n(ROI, Share)')

# Recursos
dot.edge('CENTER', 'REC', penwidth='2')
dot.edge('REC', 'CAP', label='Restricciones')
dot.node('CAP', 'Capacidad\n(Instalaciones)')
dot.edge('REC', 'MO', label='Talento')
dot.node('MO', 'Mano de Obra\n(Fuerza Laboral)')
dot.edge('REC', 'MAT', label='Insumos')
dot.node('MAT', 'Materiales\n(MRP / BOM)')

# Costos
dot.edge('CENTER', 'COS', penwidth='2')
dot.edge('COS', 'CIN', label='Holding')
dot.node('CIN', 'Costos de\nInventario')
dot.edge('COS', 'CPR', label='Operativos')
dot.node('CPR', 'Costos de\nProducción')
dot.edge('COS', 'CFA', label='Riesgo')
dot.node('CFA', 'Costos de\nFaltantes')

# Renderizar en Streamlit
st.graphviz_chart(dot, use_container_width=True)

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
        
        * <b>Planeación Agregada:</b> Equilibra la oferta y demanda a mediano plazo, definiendo niveles de producción, inventario y mano de obra.
        * <b>Objetivos Organizacionales:</b> Se traducen en KPIs como Nivel de Servicio y Rotación de Activos.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        # Gráfica de Embudo (Funnel)
        fig_strat = go.Figure(go.Funnel(
            y = ["Visión Corporativa", "Estrategia Operaciones", "Planeación Agregada", "Programa Maestro (MPS)", "Ejecución (Piso)"],
            x = [100, 80, 60, 40, 20],
            textinfo = "value+percent initial",
            marker = {"color": [COLOR_PRIMARY, "#1a5276", "#2980b9", "#5499c7", "#a9cce3"]}
        ))
        fig_strat.update_layout(title="Jerarquía de la Planeación (Despliegue)", showlegend=False, height=350)
        st.plotly_chart(fig_strat, use_container_width=True)
        st.caption("Fig 1. El 'Embudo de Decisión': Cómo la estrategia se refina hasta llegar a la orden de producción.")

# --- TAB 2: RECURSOS ---
with tab2:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Gestión de la Capacidad y Materiales")
        st.markdown("""
        <div class="big-font">
        La gestión de recursos busca asegurar la disponibilidad de los factores de producción (4M: Materiales, Máquinas, Mano de obra, Métodos).
        
        * <b>Capacidad:</b> Determina el "techo" de producción. Según <b>Chase y Jacobs (2018)</b>, la planeación debe considerar la eficiencia (OEE) y no solo la capacidad teórica.
        * <b>Materiales (MRP):</b> Transforma los requerimientos brutos en netos mediante la Lista de Materiales (BOM) y el inventario disponible.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Gráfica de Barras (Carga vs Capacidad)
        categories = ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4']
        capacity = [1000, 1000, 1000, 1000]
        load = [850, 920, 1150, 780] # Semana 3 con sobrecarga

        fig_res = go.Figure()
        fig_res.add_trace(go.Bar(x=categories, y=load, name='Carga Requerida (Demanda)', marker_color=COLOR_SECONDARY))
        fig_res.add_trace(go.Scatter(x=categories, y=capacity, mode='lines', name='Capacidad Disponible', line=dict(color='red', width=3, dash='dash')))
        
        fig_res.update_layout(title="Análisis CRP (Capacity Requirements Planning)", height=350)
        st.plotly_chart(fig_res, use_container_width=True)
        st.caption("Fig 2. Visualización de cuellos de botella: La Semana 3 excede la capacidad instalada, requiriendo horas extra.")

# --- TAB 3: COSTOS ---
with tab3:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Estructura de Costos y Optimización")
        st.markdown("""
        <div class="big-font">
        El objetivo final es minimizar el Costo Total Relevante. Existe un <i>Trade-off</i> constante entre nivel de servicio e inventario.
        
        * <b>Costos de Inventario (H):</b> Incluyen capital inmovilizado, seguros y obsolescencia. Representan entre el 15-40% del valor del producto al año.
        * <b>Costo de Faltantes:</b> Es el más crítico y difícil de medir (pérdida de clientes y reputación).
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Gráfica Donut o Treemap
        labels = ['Materia Prima', 'Mano de Obra', 'Mantenimiento Inv (H)', 'Costos de Pedir (S)', 'Faltantes']
        values = [45, 25, 15, 10, 5]
        colors = [COLOR_TERTIARY, '#e74c3c', '#ec7063', '#f1948a', '#fadbd8']

        fig_cost = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker_colors=colors)])
        fig_cost.update_layout(title="Distribución Típica del Costo Logístico", height=350)
        st.plotly_chart(fig_cost, use_container_width=True)
        st.caption("Fig 3. El costo de mantenimiento (H) es un costo oculto significativo que la planeación busca reducir.")

st.divider()

# -----------------------------------------------------------------------------
# REFERENCIAS BIBLIOGRÁFICAS (APA 7.0)
# -----------------------------------------------------------------------------
with st.expander("📚 Referencias Bibliográficas (Formato APA 7.0)", expanded=True):
    st.markdown("""
    * Chase, R. B., & Jacobs, F. R. (2018). *Administración de operaciones: Producción y cadena de suministros* (15.ª ed.). McGraw-Hill Education.
    * Chopra, S., & Meindl, P. (2016). *Administración de la cadena de suministro: Estrategia, planeación y operación* (6.ª ed.). Pearson Educación.
    * Heizer, J., Render, B., & Munson, C. (2020). *Principios de administración de operaciones* (13.ª ed.). Pearson.
    * Krajewski, L. J., Malhotra, M. K., & Ritzman, L. P. (2019). *Administración de operaciones: Procesos y cadenas de valor* (12.ª ed.). Pearson.
    """)

# Footer simple
st.markdown("---")
st.markdown("*Generado para la asignatura de Planeación y Control de la Producción | Maestría en Ingeniería*")
