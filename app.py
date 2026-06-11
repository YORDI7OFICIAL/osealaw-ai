import streamlit as st
import requests
import uuid

# Configuración de la página para que cargue rápido
st.set_page_config(page_title="OseaLaw AI - Defensa Ciudadana", page_icon="⚖️", layout="centered")

# 🔑 Clave oficial de Groq Console
LLAVE_GROQ = "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"

st.title("OSEALAW [AI] 🇻🇪")
st.write("### 🤖 Asistente Legal de Emergencia 24/7")
st.write("Analizador automático de procedimientos policiales, militares y de tránsito en Venezuela.")

# AVISO LEGAL
with st.expander("⚠️ TÉRMINOS DE USO"):
    st.caption(
        "OseaLaw AI es una plataforma informativa automatizada basada en legislación venezolana vigente. "
        "No sustituye a un abogado, es una guía de orientación ciudadana."
    )

st.write("---")

# ENTRADA ÚNICA ABIERTA
st.subheader("✍️ Escribe lo que te está exigiendo o haciendo el funcionario:")
caso = st.text_area(
    "Describe la situación detalladamente:", 
    height=110, 
    placeholder="Ej: Me quieren multar por luces led / Me dicen que no puedo grabar / Me piden extinguidores / Me quitaron los papeles..."
)

if st.button("🚨 ANALIZAR CASO Y BUSCAR LEY YA"):
    if caso:
        # Mensaje corto para no alterar al usuario
        progreso = st.info("⚡ *Procesando leyes en tiempo real...*")
        
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            ticket = f"OL-{uuid.uuid4().hex[:5].upper()}"
            
            # EL PROMPT DEFINITIVO: TOTALMENTE ABIERTO Y JURÍDICO
            prompt = (
                f"Eres un sistema informático de contraloría ciudadana y experto penal y de tránsito en Venezuela.\n"
                f"Analiza de forma totalmente abierta, objetiva y lógica el siguiente caso real en la calle:\n"
                f"SITUACIÓN: {caso}\n\n"
                f"INSTRUCCIONES DE RESPUESTA ULTRA RÁPIDA Y EXACTA:\n"
                f"1. Identifica qué ley, reglamento, decreto o gaceta oficial de Venezuela aplica exactamente para responder a esta situación específica (ej. Ley de Transporte Terrestre, Ley Orgánica de la Administración Pública, Código Penal, Resoluciones Conjuntas, etc.).\n"
                f"2. Sé extremadamente específico con la situación: si es por luces, cinturón, extintor, música alta, grabación, papeles vencidos, etc., busca la normativa exacta para ESE hecho.\n"
                f"3. Responde usando ESTRICTAMENTE esta estructura scannable (corta y directa al grano para lectura bajo presión):\n\n"
                f"### 🛑 ¿QUÉ DICE LA LEY EXACTAMENTE?\n"
                f"[Explica aquí en 2 líneas qué artículo o resolución aplica y si el funcionario TIENE o NO TIENE derecho a hacer lo que describe el usuario. Cita la ley real venezolana].\n\n"
                f"### 🛡️ TU DEFENSA EN ESTE MOMENTO:\n"
                f"[Dile al ciudadano exactamente qué responder con respeto y firmeza. Qué argumentos legales usar].\n\n"
                f"### ⚠️ ¿PUEDEN RETENER EL VEHÍCULO O DETENERTE?\n"
                f"[Aclara si esta situación amerita solo una multa administrativa o si legalmente faculta la retención].\n\n"
                f"### 📞 LÍNEA DE DENUNCIA DE EXTORSIÓN:\n"
                f"Si el funcionario te exige dinero o te amenaza ilegalmente, reporta inmediatamente a la Fiscalía del Ministerio Público: **0800-FISCA-00 (0800-34722-00)**."
            )
            
            payload = {
                "model": "llama-3.1-8b-instant", # El modelo más rápido del mercado
                "messages": [
                    {"role": "system", "content": "Eres un asistente legal automatizado de Venezuela. No saludas, no das introducciones innecesarias. Vas directo al grano con la ley aplicable al caso planteado."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.0, # Velocidad máxima y cero inventos
                "max_tokens": 500
            }
            
            headers = {'Authorization': f'Bearer {LLAVE_GROQ}', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            data = response.json()
            
            # Quitar mensaje de carga
            progreso.empty()
            
            if 'choices' in data and len(data['choices']) > 0:
                respuesta_ia = data['choices'][0]['message']['content']
                
                # Desplegar la respuesta de una vez
                st.success(f"### 📜 REPORTE LEGAL COMPLETO ({ticket})")
                st.markdown(respuesta_ia)
                
                st.write("---")
                # BOTÓN DE DESCARGA RAPIDA
                st.download_button(
                    label="📥 Guardar defensa en el teléfono", 
                    data=respuesta_ia, 
                    file_name=f"Defensa_{ticket}.txt", 
                    mime="text/plain"
                )
            else:
                st.error("❌ Error al procesar. Intenta presionar el botón nuevamente.")
        except Exception as e:
            st.error("❌ Problema de red. Dale al botón otra vez.")
    else:
        st.error("❌ Escribe la situación para poder ayudarte.")
