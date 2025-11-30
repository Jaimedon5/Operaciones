import streamlit as st
import sympy as sp
import time
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Examen Cálculo Diferencial", layout="wide")

# --- ESTILOS CSS PARA FORMULAS Y UI ---
st.markdown("""
<style>
    .big-font { font-size:20px !important; }
    .stAlert { margin-top: 20px; }
    .report-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS DE EJERCICIOS (EXTRAÍDOS DE TUS IMÁGENES) ---
# min_seconds: Tiempo mínimo estimado para un humano. Si lo hace en menos, es sospechoso.
def get_questions():
    x = sp.symbols('x')
    return [
        {
            "id": 1,
            "topic": "Límites",
            "latex": r"\lim_{x \to 2} (3x - 9)",
            "correct_expr": -3,
            "type": "value",
            "min_seconds": 10, 
            "hint": "Evalúa directamente el valor de x en la función."
        },
        {
            "id": 2,
            "topic": "Derivada (Producto)",
            "latex": r"f(x) = x \sin(x)",
            "func": x * sp.sin(x),
            "correct_expr": sp.sin(x) + x * sp.cos(x),
            "type": "derivative",
            "min_seconds": 25, 
            "hint": "Usa la regla del producto: u'v + uv'"
        },
        {
            "id": 3,
            "topic": "Derivada (Regla de la Cadena)",
            "latex": r"f(x) = (x^3 + x^2)^3",
            "func": (x**3 + x**2)**3,
            "correct_expr": 3 * (x**3 + x**2)**2 * (3*x**2 + 2*x),
            "type": "derivative",
            "min_seconds": 45,
            "hint": "Baja el exponente, resta uno, y multiplica por la derivada de lo de adentro."
        },
        {
            "id": 4,
            "topic": "Derivada (Cociente Trig)",
            "latex": r"f(x) = \frac{\sin(5x)}{\cos(6x)}",
            "func": sp.sin(5*x) / sp.cos(6*x),
            "correct_expr": sp.diff(sp.sin(5*x) / sp.cos(6*x), x),
            "type": "derivative",
            "min_seconds": 60,
            "hint": "Regla del cociente: (u'v - uv') / v^2. Cuidado con la cadena en los argumentos."
        },
        {
            "id": 5,
            "topic": "Extremos Relativos (Puntos Críticos)",
            "latex": r"f(x) = -x^2 + 2x + 1 \quad (\text{Encuentra el valor de x donde f'(x)=0})",
            "func": -x**2 + 2*x + 1,
            "correct_expr": 1, 
            "type": "value",
            "min_seconds": 30,
            "hint": "Deriva la función e iguala a cero para despejar x."
        }
    ]

# --- FUNCIONES DE AYUDA MATEMÁTICA ---
def parse_input(user_str):
    """Limpia y convierte texto del usuario a expresión SymPy"""
    try:
        # Reemplazar notación común que Python no entiende nativamente
        clean_str = user_str.replace("^", "**") 
        clean_str = clean_str.replace("sen", "sin") # Español a Inglés
        
        # Transformaciones para permitir 2x en lugar de 2*x
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
        transformations = (standard_transformations + (implicit_multiplication_application,))
        
        expr = parse_expr(clean_str, transformations=transformations)
        return expr
    except:
        return None

def check_answer(user_input, correct_expr, q_type):
    x = sp.symbols('x')
    user_expr = parse_input(user_input)
    
    if user_expr is None:
        return False, "Error de sintaxis"

    if q_type == "derivative" or q_type == "value":
        # Comparamos si la diferencia es 0 (son equivalentes)
        # simplify(user - correct) es muy potente, maneja factorizaciones diferentes
        diff = sp.simplify(user_expr - correct_expr)
        return (diff == 0), user_expr
    
    return False, "Tipo desconocido"

# --- INTERFAZ DE GRÁFICA INTERACTIVA ---
def plot_function(func_expr):
    x_sym = sp.symbols('x')
    f_lamb = sp.lambdify(x_sym, func_expr, "numpy")
    
    x_vals = np.linspace(-10, 10, 400)
    try:
        y_vals = f_lamb(x_vals)
        # Limpiar valores muy altos para la gráfica (asíntotas)
        y_vals[y_vals > 50] = np.nan
        y_vals[y_vals < -50] = np.nan
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='f(x)'))
        fig.update_layout(
            title="Visualización Interactiva de f(x)",
            xaxis_title="x",
            yaxis_title="f(x)",
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.warning("No se pudo generar la gráfica para esta función compleja.")

# --- LÓGICA DE ESTADO (SESSION STATE) ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.results = []
    st.session_state.exam_start = time.time()
    st.session_state.q_start_time = time.time()
    st.session_state.finished = False

questions = get_questions()

# --- VISTA PRINCIPAL ---
if not st.session_state.finished:
    q_data = questions[st.session_state.current_q]
    
    # Header y Progreso
    st.title(f"Ejercicio {st.session_state.current_q + 1} de {len(questions)}")
    st.progress((st.session_state.current_q) / len(questions))
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Problema:")
        st.latex(q_data['latex'])
        
        st.info("Instrucciones: Escribe tu respuesta abajo. Puedes usar '^' para potencias (ej: x^2) y 'sen' o 'sin'.")
        
        # Input del usuario
        user_response = st.text_input("Tu respuesta:", key=f"q_{st.session_state.current_q}")
        
        if st.button("Enviar Respuesta"):
            # 1. Calcular tiempo
            end_time = time.time()
            time_taken = end_time - st.session_state.q_start_time
            
            # 2. Validar respuesta
            is_correct, parsed_val = check_answer(user_response, q_data['correct_expr'], q_data['type'])
            
            # 3. Guardar logs para análisis forense
            flag = "NORMAL"
            if time_taken < q_data['min_seconds']:
                flag = "SOSPECHOSO (Muy rápido)"
            elif time_taken > (q_data['min_seconds'] * 10):
                flag = "LENTO (Posible distracción)"
                
            st.session_state.results.append({
                "Pregunta": q_data['latex'],
                "Correcta": is_correct,
                "Tiempo (s)": round(time_taken, 2),
                "Tiempo Min Esperado": q_data['min_seconds'],
                "Estado": flag,
                "Respuesta Alumno": user_response
            })
            
            if is_correct:
                st.session_state.score += 1
                st.success("¡Correcto!")
            else:
                st.error(f"Incorrecto. Revisa tu álgebra.")
            
            # Pausa breve para ver el mensaje y avanzar
            time.sleep(1.5)
            
            # Avanzar
            if st.session_state.current_q < len(questions) - 1:
                st.session_state.current_q += 1
                st.session_state.q_start_time = time.time()
                st.rerun()
            else:
                st.session_state.finished = True
                st.rerun()

    with col2:
        # Gráfica Interactiva (Si aplica)
        if "func" in q_data:
            st.markdown("### 📊 Análisis Gráfico Interactivo")
            st.caption("Usa el mouse para hacer zoom e inspeccionar la curva.")
            plot_function(q_data['func'])
        else:
            st.markdown("### Análisis")
            st.write("Este ejercicio es numérico, no requiere gráfica compleja.")

else:
    # --- PANTALLA DE RESULTADOS Y AUDITORÍA ---
    st.title("Resultados del Examen")
    
    total_q = len(questions)
    final_score = (st.session_state.score / total_q) * 100
    
    st.metric(label="Calificación Final", value=f"{final_score}%")
    
    st.divider()
    
    st.subheader("🕵️ Auditoría de Integridad y Tiempos")
    st.write("A continuación se muestra el desglose del rendimiento por pregunta. Los tiempos marcados en ROJO son anomalías estadísticas (posible trampa).")
    
    df = pd.DataFrame(st.session_state.results)
    
    # Visualización de la tabla con colores condicionales
    def color_coding(row):
        color = ''
        if "SOSPECHOSO" in row['Estado']:
            color = 'background-color: #ffcccc' # Rojo claro
        elif not row['Correcta']:
            color = 'background-color: #fee' # Muy claro para error
        return [color] * len(row)

    st.dataframe(df.style.apply(color_coding, axis=1), use_container_width=True)
    
    # Análisis de banderas
    sospechosos = df[df['Estado'].str.contains("SOSPECHOSO")]
    if not sospechosos.empty:
        st.warning(f"⚠️ ATENCIÓN PROFESOR: Se detectaron {len(sospechosos)} respuestas ingresadas en tiempos humanamente imposibles para el nivel de dificultad.")
    else:
        st.success("✅ Análisis de Tiempos: Comportamiento temporal consistente con resolución humana.")

    if st.button("Reiniciar Examen"):
        st.session_state.clear()
        st.rerun()