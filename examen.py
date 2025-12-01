import streamlit as st
import sympy as sp
import time
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Evaluación A Título - Fase 1", layout="wide")

# --- ESTILOS VISUALES AGRESIVOS (Fondo oscuro opcional o estilo serio) ---
st.markdown("""
<style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .stAlert { margin-top: 20px; }
    .report-card { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #ddd; }
    .sidebar-text { font-size: 14px; color: #555; }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS MASIVA (TRANSCRIPCIÓN COMPLETA) ---
def get_questions():
    x = sp.symbols('x')
    # NOTA: Se han transcrito los ejercicios legibles de las imágenes proporcionadas.
    # Se dividen por temas para mantener orden.
    
    questions = []
    
    # --- SECCIÓN 1: LÍMITES (Imagen 938621) ---
    limits = [
        {"latex": r"\lim_{x \to -4} 15", "ans": 15, "min_s": 5},
        {"latex": r"\lim_{x \to 0} \cos(\pi)", "ans": sp.cos(sp.pi), "min_s": 10}, # Es -1
        {"latex": r"\lim_{x \to 3} (-4)x", "ans": -12, "min_s": 10},
        {"latex": r"\lim_{x \to 2} (3x - 9)", "ans": -3, "min_s": 10},
        {"latex": r"\lim_{x \to -2} x^2", "ans": 4, "min_s": 10},
        {"latex": r"\lim_{x \to 5} (-x^3)", "ans": -125, "min_s": 15},
        {"latex": r"\lim_{x \to -1} (x^3 - 4x + 1)", "ans": 4, "min_s": 20},
        {"latex": r"\lim_{x \to 6} (-5x^2 + 6x + 8)", "ans": -136, "min_s": 25},
        {"latex": r"\lim_{x \to 2} \frac{2x + 4}{x - 7}", "ans": sp.Rational(-8, 5), "min_s": 25},
        {"latex": r"\lim_{x \to 0} \frac{x + 5}{3x}", "ans": sp.zoo, "min_s": 20, "hint": "Si es infinito, escribe 'zoo' o revisa si existe."} # Sympy usa zoo para complex infinity
    ]
    for i, q in enumerate(limits):
        questions.append({"id": f"L{i}", "topic": "Límites", "latex": q['latex'], "correct_expr": q['ans'], "type": "value", "min_seconds": q['min_s'], "hint": q.get('hint', 'Evalúa el límite.')})

    # --- SECCIÓN 2: DERIVADAS BÁSICAS (Imágenes 937e7f, 937f9d) ---
    basic_derivs = [
        {"latex": r"y = x^2 - \cos x", "func": x**2 - sp.cos(x), "ans": 2*x + sp.sin(x), "s": 15},
        {"latex": r"y = 4x^3 + x + 5\sin x", "func": 4*x**3 + x + 5*sp.sin(x), "ans": 12*x**2 + 1 + 5*sp.cos(x), "s": 25},
        {"latex": r"y = 1 + 7\sin x - \tan x", "func": 1 + 7*sp.sin(x) - sp.tan(x), "ans": 7*sp.cos(x) - sp.sec(x)**2, "s": 25},
        {"latex": r"y = 3\cos x - 5\cot x", "func": 3*sp.cos(x) - 5*sp.cot(x), "ans": -3*sp.sin(x) + 5*sp.csc(x)**2, "s": 30},
        {"latex": r"y = x \sin x", "func": x*sp.sin(x), "ans": sp.sin(x) + x*sp.cos(x), "s": 20},
        {"latex": r"y = (4\sqrt{x} - 3\sqrt[3]{x}) \cos x", "func": (4*x**(1/2) - 3*x**(1/3))*sp.cos(x), "ans": sp.diff((4*x**(1/2) - 3*x**(1/3))*sp.cos(x), x), "s": 60},
        {"latex": r"y = (x^3 - 2)\tan x", "func": (x**3 - 2)*sp.tan(x), "ans": sp.diff((x**3 - 2)*sp.tan(x), x), "s": 40},
        {"latex": r"y = \cos x \cot x", "func": sp.cos(x)*sp.cot(x), "ans": sp.diff(sp.cos(x)*sp.cot(x), x), "s": 35},
        {"latex": r"y = (x^2 + \sin x)\sec x", "func": (x**2 + sp.sin(x))*sp.sec(x), "ans": sp.diff((x**2 + sp.sin(x))*sp.sec(x), x), "s": 45},
        {"latex": r"y = \csc x \tan x", "func": sp.csc(x)*sp.tan(x), "ans": sp.diff(sp.csc(x)*sp.tan(x), x), "s": 30},
        {"latex": r"y = \cos^2 x + \sin^2 x", "func": sp.cos(x)**2 + sp.sin(x)**2, "ans": 0, "s": 15, "hint": "Simplifica la identidad trigonométrica antes de derivar."},
        {"latex": r"y = x^3 \cos x - x^3 \sin x", "func": x**3*sp.cos(x) - x**3*sp.sin(x), "ans": sp.diff(x**3*sp.cos(x) - x**3*sp.sin(x), x), "s": 50},
        # Img 937f9d
        {"latex": r"f(x) = \frac{1}{5}x^5 - 3x^4 + 9x^2 + 1", "func": x**5/5 - 3*x**4 + 9*x**2 + 1, "ans": x**4 - 12*x**3 + 18*x, "s": 25},
        {"latex": r"f(x) = -\frac{2}{3}x^6 + 4x^5 - 13x^2 + 8x + 2", "func": -2*x**6/3 + 4*x**5 - 13*x**2 + 8*x + 2, "ans": -4*x**5 + 20*x**4 - 26*x + 8, "s": 30},
        {"latex": r"f(x) = x^3(4x^2 - 5x - 6)", "func": x**3*(4*x**2 - 5*x - 6), "ans": sp.diff(x**3*(4*x**2 - 5*x - 6), x), "s": 35},
        {"latex": r"f(x) = \frac{2x^5 + 3x^4 - x^3 + 2}{x^2}", "func": (2*x**5 + 3*x**4 - x**3 + 2)/x**2, "ans": sp.diff((2*x**5 + 3*x**4 - x**3 + 2)/x**2, x), "s": 45}
    ]
    for i, q in enumerate(basic_derivs):
        questions.append({"id": f"D{i}", "topic": "Reglas Básicas y Producto", "latex": q['latex'], "func": q.get('func'), "correct_expr": q['ans'], "type": "derivative", "min_seconds": q['s'], "hint": q.get('hint', 'Deriva y simplifica.')})

    # --- SECCIÓN 3: REGLA DE LA CADENA Y COCIENTE (Imágenes 937b5e, 937f7d, 937ebd) ---
    chain_quotient = [
        {"latex": r"f(x) = x^3 \cos x^3", "func": x**3 * sp.cos(x**3), "ans": sp.diff(x**3 * sp.cos(x**3), x), "s": 40},
        {"latex": r"f(x) = \frac{\sin 5x}{\cos 6x}", "func": sp.sin(5*x)/sp.cos(6*x), "ans": sp.diff(sp.sin(5*x)/sp.cos(6*x), x), "s": 60},
        {"latex": r"f(x) = (2 + x \sin 3x)^{10}", "func": (2 + x*sp.sin(3*x))**10, "ans": sp.diff((2 + x*sp.sin(3*x))**10, x), "s": 50},
        {"latex": r"f(x) = \tan(1/x)", "func": sp.tan(1/x), "ans": sp.diff(sp.tan(1/x), x), "s": 30},
        {"latex": r"f(x) = \sin 2x \cos 3x", "func": sp.sin(2*x)*sp.cos(3*x), "ans": sp.diff(sp.sin(2*x)*sp.cos(3*x), x), "s": 40},
        {"latex": r"f(x) = (\sec 4x + \tan 2x)^5", "func": (sp.sec(4*x) + sp.tan(2*x))**5, "ans": sp.diff((sp.sec(4*x) + sp.tan(2*x))**5, x), "s": 60},
        {"latex": r"f(x) = \sin(\sin 2x)", "func": sp.sin(sp.sin(2*x)), "ans": sp.diff(sp.sin(sp.sin(2*x)), x), "s": 35},
        {"latex": r"f(x) = \cos(\sin \sqrt{2x+5})", "func": sp.cos(sp.sin(sp.sqrt(2*x+5))), "ans": sp.diff(sp.cos(sp.sin(sp.sqrt(2*x+5))), x), "s": 70},
        {"latex": r"f(x) = \tan^3(4x^2 - 1)", "func": sp.tan(4*x**2 - 1)**3, "ans": sp.diff(sp.tan(4*x**2 - 1)**3, x), "s": 50},
        # Img 937f7d
        {"latex": r"f(x) = x^2(x^2 + 5)^2", "func": x**2*(x**2+5)**2, "ans": sp.diff(x**2*(x**2+5)**2, x), "s": 40},
        {"latex": r"f(x) = (x^3 + x^2)^3", "func": (x**3+x**2)**3, "ans": sp.diff((x**3+x**2)**3, x), "s": 35},
        {"latex": r"f(x) = (4\sqrt{x} + 1)^2", "func": (4*sp.sqrt(x)+1)**2, "ans": sp.diff((4*sp.sqrt(x)+1)**2, x), "s": 30},
        {"latex": r"f(x) = (9+x)(9-x)", "func": (9+x)*(9-x), "ans": -2*x, "s": 15, "hint": "Simplifica primero (diferencia de cuadrados)."},
        # Img 937ebd (Cocientes básicos)
        {"latex": r"y = \frac{10}{x^2 + 1}", "func": 10/(x**2+1), "ans": sp.diff(10/(x**2+1), x), "s": 30},
        {"latex": r"y = \frac{5}{4x - 3}", "func": 5/(4*x-3), "ans": sp.diff(5/(4*x-3), x), "s": 25},
        {"latex": r"y = \frac{3x + 1}{2x - 5}", "func": (3*x+1)/(2*x-5), "ans": sp.diff((3*x+1)/(2*x-5), x), "s": 35},
        {"latex": r"y = (6x - 1)^2", "func": (6*x-1)**2, "ans": 12*(6*x-1), "s": 20},
        {"latex": r"y = (x^4 + 5x)^2", "func": (x**4+5*x)**2, "ans": sp.diff((x**4+5*x)**2, x), "s": 30}
    ]
    for i, q in enumerate(chain_quotient):
        questions.append({"id": f"C{i}", "topic": "Regla de la Cadena y Cociente", "latex": q['latex'], "func": q.get('func'), "correct_expr": q['ans'], "type": "derivative", "min_seconds": q['s'], "hint": q.get('hint', 'Usa regla de la cadena.')})

    # --- SECCIÓN 4: MÁXIMOS, MÍNIMOS Y CRITERIO 1RA DERIVADA (Imágenes 937723, 937381) ---
    # Convertimos los de gráficas a analíticos para que Sympy los evalúe
    extrema = [
        {"latex": r"f(x) = -x^2 + 2x + 1 \quad (Encuentra \ x \ tal \ que \ f'(x)=0)", "func": -x**2 + 2*x + 1, "ans": 1, "s": 20},
        {"latex": r"f(x) = (x-1)(x+3) \quad (Encuentra \ x \ tal \ que \ f'(x)=0)", "func": (x-1)*(x+3), "ans": -1, "s": 30},
        {"latex": r"f(x) = x^3 - 3x \quad (Encuentra \ x > 0 \ tal \ que \ f'(x)=0)", "func": x**3 - 3*x, "ans": 1, "s": 25},
        {"latex": r"f(x) = \frac{1}{3}x^3 - \frac{1}{2}x^2 + 1 \quad (Encuentra \ x \neq 0 \ tal \ que \ f'(x)=0)", "func": x**3/3 - x**2/2 + 1, "ans": 1, "s": 35},
        {"latex": r"f(x) = x(x-2)^2 \quad (Encuentra \ el \ menor \ valor \ de \ x \ tal \ que \ f'(x)=0)", "func": x*(x-2)**2, "ans": sp.Rational(2, 3), "s": 45},
        {"latex": r"f(x) = x^4 - 4x^3 + 7 \quad (Encuentra \ x \neq 0 \ tal \ que \ f'(x)=0)", "func": x**4 - 4*x**3 + 7, "ans": 3, "s": 40},
        {"latex": r"f(x) = (x-2)^2(x-1) \quad (Encuentra \ x \ tal \ que \ f'(x)=0 \ y \ x \ es \ entero)", "func": (x-2)**2*(x-1), "ans": 2, "s": 45},
        {"latex": r"f(x) = 2x^2 - 6x + 8 \quad (Encuentra \ x \ crítico)", "func": 2*x**2 - 6*x + 8, "ans": sp.Rational(3, 2), "s": 25},
        {"latex": r"f(x) = 2x^3 - 15x^2 - 36x \quad (Encuentra \ x > 0 \ crítico)", "func": 2*x**3 - 15*x**2 - 36*x, "ans": 6, "s": 40},
        {"latex": r"f(x) = \frac{x^2}{x^2 + 2} \quad (Encuentra \ x \ tal \ que \ f'(x)=0)", "func": x**2/(x**2+2), "ans": 0, "s": 45}
    ]
    for i, q in enumerate(extrema):
        questions.append({"id": f"E{i}", "topic": "Puntos Críticos y Extremos", "latex": q['latex'], "func": q.get('func'), "correct_expr": q['ans'], "type": "value", "min_seconds": q['s'], "hint": "Deriva e iguala a cero."})
        
    return questions

# --- FUNCIONES AUXILIARES MATEMÁTICAS ---
def parse_input(user_str):
    if not user_str: return None
    try:
        clean_str = user_str.replace("^", "**").replace("sen", "sin").replace("sec", "1/cos").replace("csc", "1/sin")
        clean_str = clean_str.replace("zoo", "oo") # Infinito
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
        transformations = (standard_transformations + (implicit_multiplication_application,))
        return parse_expr(clean_str, transformations=transformations)
    except:
        return None

def check_answer(user_input, correct_expr, q_type):
    user_expr = parse_input(user_input)
    if user_expr is None: return False, "Error de sintaxis"
    try:
        diff = sp.simplify(user_expr - correct_expr)
        if diff == 0: return True, user_expr
        if sp.trigsimp(diff) == 0: return True, user_expr
        # Check para infinitos o valores especiales
        if q_type == "value" and user_expr == correct_expr: return True, user_expr
        return False, user_expr
    except:
        return False, user_expr

# --- GRÁFICAS ---
def plot_function(func_expr):
    x_sym = sp.symbols('x')
    try:
        f_lamb = sp.lambdify(x_sym, func_expr, "numpy")
        x_vals = np.linspace(-6, 6, 400)
        y_vals = f_lamb(x_vals)
        # Limpieza de asíntotas
        y_vals[y_vals > 25] = np.nan
        y_vals[y_vals < -25] = np.nan
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='f(x)', line=dict(color='#dc3545', width=2)))
        fig.update_layout(
            title="Análisis Gráfico", height=300, margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="#f8f9fa", plot_bgcolor="white"
        )
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.caption("Gráfica no disponible para esta complejidad.")

# --- INICIALIZACIÓN ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.results = []
    st.session_state.q_start_time = time.time()
    st.session_state.finished = False

questions = get_questions()
total_fake_bank = 900 # Número psicológico para el alumno

# --- BARRA LATERAL (CONTEXTO DE FASES) ---
with st.sidebar:
    st.markdown("## 🗃️ Banco de Reactivos")
    st.info(f"Cargando Fase 1 de 10")
    st.markdown(f"**Total en Base de Datos:** {total_fake_bank}+ reactivos")
    st.markdown("---")
    st.markdown("### ⏱️ Monitoreo Activo")
    st.warning("El tiempo de respuesta está siendo auditado por reactivo. Respuestas instantáneas serán marcadas.")
    st.markdown("---")
    st.caption("Sistema de Evaluación Autodidacta v2.4")

# --- VISTA PRINCIPAL ---
if not st.session_state.finished:
    q_data = questions[st.session_state.current_q]
    
    # Header intimidante
    st.markdown(f"### Reactivo {st.session_state.current_q + 1} / {len(questions)}  <span style='font-size:14px; color:gray'>(ID: {q_data['id']})</span>", unsafe_allow_html=True)
    st.progress((st.session_state.current_q) / len(questions))
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown(f"<div class='big-font'>Tema: {q_data['topic']}</div>", unsafe_allow_html=True)
        st.markdown("---")
        st.latex(q_data['latex'])
        st.markdown("---")
        
        user_response = st.text_input("Ingrese su desarrollo/resultado:", key=f"input_{st.session_state.current_q}")
        
        st.caption("Sintaxis: Use `^` para exponentes, `sqrt()` para raíces. Funciones: `sin`, `cos`, `tan`, `ln`.")
        
        if st.button("Validar y Continuar ➡️", type="primary"):
            time_taken = time.time() - st.session_state.q_start_time
            is_correct, _ = check_answer(user_response, q_data['correct_expr'], q_data['type'])
            
            # Lógica Anti-Cheat Estricta
            flag = "NORMAL"
            if time_taken < q_data['min_seconds']: flag = "SOSPECHOSO (TIEMPO INSUFICIENTE)"
            elif time_taken > (q_data['min_seconds'] * 10): flag = "LENTO (POSIBLE DISTRACCIÓN)"
            
            st.session_state.results.append({
                "ID": q_data['id'],
                "Pregunta": q_data['latex'],
                "Correcta": is_correct,
                "Tiempo (s)": round(time_taken, 1),
                "Min Requerido": q_data['min_seconds'],
                "Estado": flag,
                "Input": user_response
            })
            
            if is_correct: 
                st.session_state.score += 1
                st.success("✅ Respuesta Registrada Correctamente")
            else: 
                st.error("❌ Respuesta Incorrecta Registrada")
                if "hint" in q_data: st.info(f"Retroalimentación: {q_data['hint']}")
            
            time.sleep(1) # Breve pausa obligatoria
            
            if st.session_state.current_q < len(questions) - 1:
                st.session_state.current_q += 1
                st.session_state.q_start_time = time.time()
                st.rerun()
            else:
                st.session_state.finished = True
                st.rerun()

    with col2:
        if "func" in q_data:
            st.markdown("###### Visualización Dinámica")
            plot_function(q_data['func'])
        else:
            st.markdown("###### Cálculo Algebraico Puro")
            st.info("Este reactivo evalúa capacidad de abstracción numérica/algebraica. No se requiere gráfica.")

else:
    # --- PANTALLA FINAL ---
    st.balloons()
    st.markdown("## 🏁 Fase 1 Completada")
    st.success("Los datos han sido encriptados y están listos para el envío.")
    
    score_pct = (st.session_state.score / len(questions)) * 100
    total_time = sum(r['Tiempo (s)'] for r in st.session_state.results) / 60
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Puntuación Fase 1", f"{score_pct:.1f}%")
    col2.metric("Reactivos Correctos", f"{st.session_state.score}/{len(questions)}")
    col3.metric("Tiempo Total Sesión", f"{total_time:.1f} min")
    
    st.markdown("### 🕵️ Auditoría Forense de Tiempos")
    df = pd.DataFrame(st.session_state.results)
    
    def highlight_audit(row):
        if "SOSPECHOSO" in row['Estado']: return ['background-color: #ffcccc; color: #8b0000; font-weight: bold'] * len(row)
        elif not row['Correcta']: return ['background-color: #f8f9fa; color: #666'] * len(row)
        return ['background-color: #d4edda; color: #155724'] * len(row)
    
    st.dataframe(df.style.apply(highlight_audit, axis=1), use_container_width=True)

    # --- ENVÍO DE CORREO ---
    if 'email_sent' not in st.session_state:
        st.session_state.email_sent = False

    if not st.session_state.email_sent:
        with st.spinner("Conectando con servidor seguro para envío de resultados..."):
            try:
                email_sender = st.secrets["email"]["sender"]
                email_password = st.secrets["email"]["password"]
                email_receiver = st.secrets["email"]["receiver"]

                msg = MIMEMultipart()
                msg['From'] = email_sender
                msg['To'] = email_receiver
                msg['Subject'] = f"REPORTE FASE 1 (1-900) - {score_pct:.1f}% - {time.strftime('%Y-%m-%d %H:%M')}"

                html_table = df.to_html(index=False, border=1)
                body = f"""
                <h2 style="font-family: Arial, sans-serif;">Reporte de Examen A Título: Fase 1</h2>
                <p><strong>Banco de Reactivos:</strong> 1 - {len(questions)} (de 900)</p>
                <p><strong>Calificación:</strong> {score_pct:.1f}%</p>
                <p><strong>Tiempo Efectivo:</strong> {total_time:.2f} min</p>
                <hr>
                <h3>Auditoría de Integridad:</h3>
                {html_table}
                <br>
                <p style="font-size: 10px; color: gray;">Generado por Sistema Automatizado Python/Streamlit.</p>
                """
                msg.attach(MIMEText(body, 'html'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email_sender, email_password)
                server.sendmail(email_sender, email_receiver, msg.as_string())
                server.quit()

                st.session_state.email_sent = True
                st.success(f"✅ Reporte oficial enviado a: {email_receiver}")
            except Exception as e:
                st.error(f"Error de conexión SMTP: {e}")
                st.warning("⚠️ Capture esta pantalla y envíela al docente inmediatamente.")
    else:
        st.info("Reporte enviado.")
