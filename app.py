import streamlit as st
import requests
import urllib.parse
import uuid

# Configuración de la página
st.set_page_config(page_title="OseaLaw AI - Defensa Ciudadana", page_icon="⚖️", layout="centered")

# 🔑 Clave oficial de Groq Console
LLAVE_GROQ = "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"

st.title("OSEALAW [AI] 🇻🇪")
st.write("### 🤖 Asistente Legal de Emergencia contra el Abuso de Poder")
st.write("Una herramienta libre para proteger a los conductores y motorizados de Venezuela.")

# AVISO LEGAL DE PROTECCIÓN
with st.expander("⚠️ TÉRMINOS DE USO Y DESCARGO DE RESPONSABILIDAD"):
    st.warning(
        "OseaLaw AI es una plataforma tecnológica de información automatizada. "
        "El sistema compila normativas vigentes en la República Bolivariana de Venezuela basándose en Gacetas Oficiales. "
        "NO es un bufete de abogados y NO sustituye a un profesional colegiado. El uso de esta información es responsabilidad del usuario."
    )

st.write("---")

# FORMULARIO EXPRESS PARA EL CIUDADANO EN LA CALLE
st.subheader("✍️ Describe tu situación actual en la alcabala o punto de control:")
nombre_usuario = st.text_input("👤 Tu Nombre (Opcional):", value="Ciudadano")
caso = st.text_area(
    "¿Qué está sucediendo?", 
    height=120, 
    placeholder="Ejemplo: Me pararon porque no tengo el casco y me quieren retener la moto o pedirme dinero..."
)

if st.button("🚨 CONSULTAR LEY EN TIEMPO REAL"):
    if caso:
        st.info("⏳ *Buscando normativas, resoluciones y gacetas oficiales...*")
        
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            ticket_servidor = f"OL-FREE-{uuid.uuid4().hex[:6].upper()}"
            
            # PROMPT ADAPTADO PARA RESPUESTAS DE DEFENSA INMEDIATA
            prompt = (
                f"Actúas como un sistema informático de contraloría ciudadana y defensa del conductor en Venezuela.\n"
                f"Genera un INFORME DE EMERGENCIA para el ciudadano {nombre_usuario}.\n\n"
                f"Situación reportada: {caso}\n\n"
                f"INSTRUCCIONES DE REDACCIÓN COMPORTAMIENTO LEGAL:\n"
                f"1. Sé directo, claro y contundente. El ciudadano está en la calle bajo presión, necesita saber YA sus derechos.\n"
                f"2. Explica claramente si la autoridad PUEDE o NO PUEDE hacer lo que pretende (ej. retener el vehículo, imponer multas locas, pedir dinero).\n"
                f"3. CITA LEYES REALES VENEZOLANAS:\n"
                f"   - Si es por NO USAR CASCO o infracciones menores, explica que según el Artículo 181 de la Ley de Transporte Terrestre, las infracciones conllevan MULTA administrativa, NO la retención o decomiso de la moto (a menos que no tenga papeles o maneje ebrio).\n"
                f"   - Si el funcionario prohíbe grabar, cita el Artículo 20 de la Resolución Conjunta N° 109 (Defensa e Interiores) que avala el derecho ciudadano a grabar en video los procedimientos policiales.\n"
                f"4. Indica al ciudadano mantener la calma, hablar con respeto pero con base legal, y menciona los números o entes para denunciar extorsión (Ministerio Público / Fiscalía)."
            )
            
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "Eres un sistema automatizado de contraloría ciudadana. Tu deber es informar de manera fría, objetiva y exacta sobre los derechos de los conductores en Venezuela basados en leyes y gacetas reales."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1
            }
            
            headers = {'Authorization': f'Bearer {LLAVE_GROQ}', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            data = response.json()
            
            if 'choices' in data and len(data['choices']) > 0:
                respuesta_ia = data['choices'][0]['message']['content']
                
                # Cuadro de respuesta destacado
                st.success("### 📜 TU DEFENSA LEGAL EN TIEMPO REAL:")
                st.markdown(respuesta_ia)
                
                st.markdown("---")
                st.caption(f"Identificador de consulta: {ticket_servidor} | Amparado en el Art. 51 y 143 de la CRBV.")
                
                # BOTÓN DE DESCARGA DIRECTA Y GRATIS
                st.download_button(
                    label="📥 Guardar esta Defensa en el Teléfono", 
                    data=respuesta_ia, 
                    file_name=f"Defensa_OseaLaw_{ticket_servidor}.txt", 
                    mime="text/plain"
                )
            else:
                st.error("❌ Hubo un problema al conectar con el cerebro de la IA. Intenta de nuevo.")
        except Exception as e:
            st.error(f"❌ Error de conexión: {str(e)}")
    else:
        st.error("❌ Por favor, escribe lo que te está pasando para poder buscar la ley.")
