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
# MENÚ LATERAL
# -----------------------------------------------------------------------------
st.sidebar.title("Menu")
section = st.sidebar.radio(
    "Navegacion",
    ["Portada", "Semana 1", "Semana 2", "Semana 3", "Semana 4", "Bibliografía"],
    index=0
)

if section == "Portada":
    # Container principal de portada - sin caracteres especiales en HTML
    container_html = "<div style='padding: 20px 40px; background-color: rgba(15, 23, 42, 0.5); border-radius: 8px;'>"
    
    # Universidad
    container_html += "<div style='text-align: center; margin-bottom: 10px;'>"
    container_html += "<p style='color: var(--gold); font-size: 1.3rem; font-weight: bold; margin: 0;'>UNIVERSIDAD UO GLOBAL</p>"
    container_html += "<p style='color: var(--text); font-size: 0.95rem; margin: 5px 0 0 0;'>Maestria en Ingenieria Industrial</p>"
    container_html += "<p style='color: var(--muted); font-size: 0.9rem; margin: 2px 0 0 0;'>Administracion de la Produccion y las Operaciones</p>"
    container_html += "</div>"
    
    # Separator
    container_html += "<hr style='border: 1px solid var(--border); margin: 15px 0;'>"
    
    # Titulo
    container_html += "<div style='text-align: center; margin-bottom: 10px;'>"
    container_html += "<h1 style='color: var(--accent); font-size: 1.8rem; margin: 0 0 5px 0;'>PROYECTO INTEGRADOR</h1>"
    container_html += "<p style='color: var(--text); font-size: 1rem; margin: 0;'>Sistema Integral de Planeacion de la Produccion</p>"
    container_html += "</div>"
    
    # Separator
    container_html += "<hr style='border: 1px solid var(--border); margin: 15px 0;'>"
    
    # Docente y Autor
    container_html += "<div style='display: flex; justify-content: space-between; margin: 15px 0;'>"
    container_html += "<div style='text-align: left; flex: 1;'>"
    container_html += "<p style='color: var(--text); font-size: 0.9rem; font-weight: bold; margin: 0;'>Docente:</p>"
    container_html += "<p style='color: var(--gold); font-size: 0.95rem; margin: 2px 0 0 0;'>Dra. Diana Faviola Olea Flores</p>"
    container_html += "</div>"
    container_html += "<div style='text-align: right; flex: 1;'>"
    container_html += "<p style='color: var(--text); font-size: 0.9rem; font-weight: bold; margin: 0;'>Autor:</p>"
    container_html += "<p style='color: var(--gold); font-size: 0.95rem; margin: 2px 0 0 0;'>Ing. Jaime Silva Betancourt</p>"
    container_html += "<p style='color: var(--muted); font-size: 0.85rem; margin: 2px 0 0 0;'>Matricula: 42500289</p>"
    container_html += "</div>"
    container_html += "</div>"
    
    # Fecha
    container_html += "<div style='text-align: center; margin: 15px 0 0 0;'>"
    container_html += "<p style='color: var(--text); font-size: 0.9rem; font-weight: bold; margin: 0;'>Fecha de Entrega:</p>"
    container_html += "<p style='color: var(--accent); font-size: 0.95rem; margin: 2px 0 0 0;'>22 de febrero de 2026</p>"
    container_html += "</div>"
    container_html += "</div>"
    
    st.markdown(container_html, unsafe_allow_html=True)
    
    st.markdown("")
    
    st.subheader("Resumen Formal del Contenido")
    st.markdown("""
    Este proyecto integrador presenta un analisis exhaustivo del Sistema Integral de Planeacion de la Produccion, abordando desde 
    sus fundamentos historicos hasta la aplicacion contemporanea de tecnicas modernas de planeacion, programacion y control.
    
    El contenido esta estructurado de manera progresiva:
    
    * **Semana 1:** Linea de tiempo que contextualiza la evolucion historica de la administracion de operaciones desde 1750 hasta la actualidad.
    * **Semana 2:** Inventarios y modelos de optimizacion (EOQ, Safety Stock, Cycle Stock).
    * **Semana 3:** Desarrollo integral del Sistema: componentes estrategicos, gestion de recursos y estructura de costos, con analisis visual y cuantitativo.
    * **Semana 4:** Plan Maestro de Produccion (PMP) y Material Requirements Planning (MRP) con ejercicios practicos y resolucion de casos.
    """)

elif section == "Semana 1":
    st.markdown("## Semana 1: Conceptos Iniciales - Línea de Tiempo Histórica")
    
    st.subheader("Introducción")
    st.markdown("""
    La administración de operaciones ha evolucionado significativamente a lo largo de más de 250 años. Desde los principios de la 
    manufactura artesanal hasta la automatización digital contemporánea, cada era ha dejado su huella en cómo planificamos y controlamos 
    la producción. Esta semana exploraremos cómo los conceptos fundamentales de la planeación se han desarrollado, permitiéndonos comprender 
    por qué los métodos modernos son efectivos.
    """)
    
    st.subheader("Desarrollo")
    st.markdown("""Haga clic en los nodos circulares de la línea de tiempo para desplegar el análisis detallado de cada período.""")

    html_path = Path(__file__).parent / "assets" / "semana_1_timeline.html"
    if html_path.exists():
        timeline_html = html_path.read_text(encoding="utf-8", errors="ignore")
        components.html(timeline_html, height=900, scrolling=True)
    else:
        st.error("No se encontro el archivo de linea de tiempo. Verifique la carpeta assets.")
    
    st.divider()
    st.subheader("Conclusión y Reflexión del Aprendizaje")
    st.markdown("""
    La evolución histórica de la administración de operaciones demuestra que cada innovación surgió en respuesta a desafíos específicos 
    de su época. La Revolución Industrial introdujo la producción en serie, el fordismo revolucionó con la estandarización, la era post-guerra 
    trajo la gestión de la calidad, y la era digital ha integrado sistemas en tiempo real. Entender esta progresión nos permite apreciar que 
    los métodos contemporáneos de planeación no surgieron del vacío, sino como refinamientos iterativos de principios fundamentales. 
    La pregunta crítica para la ingeniería moderna es: ¿cómo integramos la flexibilidad digital con la eficiencia de los sistemas clásicos?
    """)

elif section == "Semana 2":
    st.markdown("## Semana 2: Inventarios - Modelos de Optimización y Control")
    
    st.subheader("Introducción")
    st.markdown("""
    La gestión de inventarios es uno de los pilares fundamentales de la planeación de la producción. Los inventarios representan un balance 
    delicado: demasiados generan costos innecesarios, mientras que demasiado pocos resultan en faltantes y pérdida de clientes. 
    Esta semana abordaremos los modelos matemáticos que permiten optimizar esta decisión crítica.
    """)
    
    st.subheader("Desarrollo")
    st.markdown("""
    **Modelos Aplicados:**
    
    1. **EOQ (Economic Order Quantity):** Determina el lote económico que minimiza el costo total de inventario.
    2. **Safety Stock:** Calcula el inventario de seguridad para protegerse contra variabilidad en la demanda.
    3. **Cycle Stock:** Representa el inventario promedio durante el período de reorden.
    
    **Resolución de Ejercicios en Clase:**
    
    - Cálculo de EOQ para diferentes productos con demandas variadas
    - Análisis de sensibilidad: impacto de cambios en costos de ordenar y mantener
    - Determinación de puntos de reorden considerando lead time y variabilidad
    - Evaluación de políticas de inventario para múltiples artículos con restricciones presupuestarias
    
    **Corrección de Errores Identificados en Retroalimentaciones Anteriores:**
    
    Los estudiantes que cometieron errores conceptuales en la comprensión de la demanda independiente versus dependiente 
    deberán revisar la diferencia entre gestión de MTS (Make-to-Stock) versus MTO (Make-to-Order).
    """)
    
    st.divider()
    st.subheader("Conclusión y Reflexión del Aprendizaje")
    st.markdown("""
    Los modelos de optimización de inventarios demuestran que la decisión sobre "cuánto producir" no es arbitraria, sino que puede ser 
    sustentada matemáticamente. Sin embargo, en la práctica, muchas variables (cambios de mercado, estacionalidad, disponibilidad de proveedores) 
    hacen que estos modelos clásicos sean puntos de partida, no soluciones finales. La verdadera habilidad del ingeniero de producción es 
    reconocer cuándo se justifica alejarse de los modelos teóricos y adaptar la estrategia a la realidad operativa.
    """)

elif section == "Semana 3":
    # ENCABEZADO ESPECÍFICO PARA SEMANA 3
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
    
    st.divider()
    st.subheader("Conclusión y Reflexión del Aprendizaje")
    st.markdown("""
    El análisis multidimensional del sistema de planeación revela una verdad fundamental: no existe una "época de oro" en la que se puede 
    optimizar una sola variable (costo, tiempo, o calidad) sin afectar las demás. La excelencia operativa emerge de la comprensión profunda 
    de estos tradeoffs y la capacidad de equilibrar objetivos competidores. Los roles de futuro en ingeniería industrial serán aquellos 
    que puedan ver más allá de los números y entender las implicaciones humanas, ambientales y de mercado de sus decisiones. 
    La tecnología (AI, IoT, blockchain) son herramientas poderosas, pero sin una comprensión sistemática, se vuelven ineficaces.
    """)

elif section == "Semana 4":
    st.markdown("## Semana 4: Plan Maestro de Producción (PMP) y Material Requirements Planning (MRP)")
    
    st.subheader("Introducción")
    st.markdown("""
    Una vez entendemos el sistema integral y hemos optimizado los inventarios, llegamos a la etapa operativa donde los planes se convierten 
    en acciones concretas. El Plan Maestro de Producción (PMP) y el Material Requirements Planning (MRP) son los mecanismos a través de 
    los cuales la estrategia se traduce en programas de producción detallados y requisiciones de materiales. Esta semana aplicaremos estos 
    métodos a casos prácticos.
    """)
    
    st.subheader("Desarrollo")
    st.markdown("""
    **1. Plan Maestro de Producción (PMP):**
    
    Es el plan de producción expresado en términos de artículos finales. Establece el "qué" y el "cuándo" producir.
    - Horizonte: Generalmente 12-24 semanas hacia el futuro
    - Frecuencia de actualización: Semanal o quincenal
    - Input: Pronóstico de demanda + Órdenes confirmadas + Política de inventario de seguridad
    - Output: Programa de producción de artículos finales
    
    **2. Material Requirements Planning (MRP):**
    
    Transforma los requisitos del PMP en requisitos de componentes y materia prima.
    - Entrada: Estructura del producto (BOM), lead times, inventarios disponibles, PMP
    - Proceso: Desagregación de demanda independiente en demanda dependiente
    - Salida: Programas de compra / producción para cada componente
    
    **Ejercicios Realizados en Clase:**
    
    - Desarrollo de tablas y cálculos correspondientes de MRP para productos multicomponentes
    - Análisis de lead times y sus implicaciones en el horizonte de planeación
    - Ajustes aplicados conforme a observaciones previas de retroalimentación de clase
    
    **Resultados Obtenidos y Análisis:**
    
    - Se demostró cómo un retraso en el suministro de un solo componente puede disrumpar todo el PMP
    - Se ilustró el efecto "bullwhip" en cadenas de suministro multicapa
    - Se cuantificó el impacto de la reducción de lead times en mejora de responsividad
    """)
    
    st.info("""
    **Nota:** Los ejercicios aplicados en clase incluyen casos reales adaptados de la industria de manufactura, 
    permitiendo la vivencia práctica de los conceptos teóricos desarrollados en semanas anteriores.
    """)
    
    st.divider()
    st.subheader("Conclusión y Reflexión del Aprendizaje")
    st.markdown("""
    El PMP y MRP son más que herramientas de programación: representan el puente entre estrategia y ejecución. Su efectividad depende 
    criterialmente de la calidad de los datos, la actualidad de la información y la disciplina en su mantenimiento. En la era del 
    "big data" y "real-time monitoring", estos métodos clásicos continúan siendo relevantes, pero ahora pueden potenciarse con 
    inteligencia artificial para predicciones más precisas y adaptaciones automáticas. La lección fundamental es que la tecnología es 
    un amplificador: puede mejorar un proceso mal diseñado o un proceso bien diseñado, pero nunca puede compensar la falta de comprensión 
    conceptual. Como ingenieros, nuestra responsabilidad es dominar ambos: la teoría y la tecnología.
    """)

elif section == "Bibliografía":
    st.markdown("## Bibliografía Completa del Proyecto")
    st.markdown("**Formato: APA 7.0**")
    
    st.markdown("""
    ### Libros de Texto Principal
    
    Chase, R. B., & Jacobs, F. R. (2018). *Administración de operaciones: Producción y cadena de suministros* (15.ª ed.). McGraw-Hill Education.
    
    Chopra, S., & Meindl, P. (2016). *Administración de la cadena de suministro: Estrategia, planeación y operación* (6.ª ed.). Pearson Educación.
    
    Heizer, J., Render, B., & Munson, C. (2020). *Principios de administración de operaciones* (13.ª ed.). Pearson.
    
    Krajewski, L. J., Malhotra, M. K., & Ritzman, L. P. (2019). *Administración de operaciones: Procesos y cadenas de valor* (12.ª ed.). Pearson.
    
    ### Referencias Complementarias
    
    Schroeder, R. G., Goldstein, S. M., & Rungtusanatham, M. J. (2018). *Operations management in the supply chain: Decisions and cases* (7.ª ed.). McGraw-Hill.
    
    Slack, N., Brandon-Jones, A., & Johnston, R. (2019). *Operations management* (9.ª ed.). Pearson Education.
    
    Tersine, R. J. (2017). *Principles of inventory and materials management* (4.ª ed.). Prentice Hall.
    
    West, D. M. (2018). *The future of work: Robots, AI, and automation*. Brookings Institution Press.
    
    ### Artículos y Publicaciones en Revistas
    
    Bortolotti, T., Boscari, S., & Danese, P. (2015). Successful lean implementation: Organizational culture and soft lean practices. 
    *International Journal of Production Economics*, 160, 21-32.
    
    Dey, S., Biswas, S., Sarkar, A., & Mukherjee, K. (2019). Analyzing the effects of supply chain network disruption due to manufacturing 
    yield uncertainty. *International Journal of Production Research*, 57(16), 4992-5008.
    
    Gunasekaran, A., Patel, C., & McGaughey, R. (2017). A framework for supply chain performance measurement. *International Journal of 
    Production Economics*, 87(3), 333-347.
    
    Müller, R., & Turner, J. R. (2018). Leadership competency in project and program management. *Project Management Journal*. 
    Educational & Management Services.
    
    ### Normas y Estándares
    
    International Organization for Standardization (2015). *ISO 31000: Risk management - Principles and guidelines*. ISO.
    
    International Organization for Standardization (2018). *ISO 9001: Quality management systems - Requirements*. ISO.
    
    Project Management Institute (2017). *A guide to the project management body of knowledge (PMBOK Guide)* (6.ª ed.). PMI.
    
    ### Recursos de Consulta en Línea
    
    American Production and Inventory Control Society (APICS). (2023). *APICS Dictionary*. Consultado de https://www.apics.org/
    
    Council of Supply Chain Management Professionals (CSMP). (2023). *Supply Chain Management Body of Knowledge*. Consultado de 
    https://www.csmp.org/
    """)
    
    st.divider()
    st.info("""
    **Nota Metodológica:** Esta bibliografía ha sido compilada siguiendo los estándares APA 7.0. Cada referencia incluida ha sido 
    seleccionada por su relevancia teórica o práctica al contenido del curso. Se recomienda que los estudiantes complementen esta 
    bibliografía con búsquedas en bases de datos académicas como Google Scholar, JSTOR, y ResearchGate.
    """)

# Footer simple
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: var(--muted); font-size: 0.85rem;">
    <p><b>Generado para la asignatura de Administración de la Producción y las Operaciones</b></p>
    <p>Maestría en Ingeniería Industrial | Universidad UO Global</p>
    <p>Proyecto Integrador - Febrero 2026</p>
</div>
""", unsafe_allow_html=True)
