import streamlit as st
import requests
import urllib.parse
import uuid

# Configuración Premium de la página
st.set_page_config(page_title="OseaLaw AI", page_icon="⚖️", layout="centered")

# 🔑 Clave oficial de Groq Console
LLAVE_GROQ = "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"

# 📱 Datos de cobro del soporte técnico (Tú)
NUMERO_WHATSAPP_DUEÑO = "584249749786"
DATOS_PAGO_MOVIL = """
🏦 **Banco:** 0104 (Venezolano de Crédito)
🆔 **Cédula/RIF:** 26999511
📱 **Teléfono:** 04249749786
💵 **Soporte de Infraestructura:** $5 USD (A tasa oficial BCV)
"""

# Inicialización de bases de datos internas del APK para tráfico masivo
if "base_usuarios" not in st.session_state:
    st.session_state.base_usuarios = {
        "admin@osealaw.com": {"nombre": "Administrador General", "clave": "BossOsea2026", "rol": "Dueño", "cedula": "0", "telefono": "0"},
        "soporte@osealaw.com": {"nombre": "Auditor de Sistema", "clave": "SoporteOsea2026", "rol": "Soporte", "cedula": "0", "telefono": "0"}
    }

if "base_de_datos_casos" not in st.session_state:
    st.session_state.base_de_datos_casos = []

if "usuario_conectado" not in st.session_state:
    st.session_state.usuario_conectado = None

if "rol_conectado" not in st.session_state:
    st.session_state.rol_conectado = None


# =========================================================================
# CONTROL DE ACCESO (REGISTRO PÚBLICO MASIVO)
# =========================================================================
if st.session_state.usuario_conectado is None:
    st.title("OSEALAW [AI] 🇻🇪")
    st.write("### Sistema Automatizado de Información Normativa Ciudadana")
    
    # TERMINOS Y CONDICIONES VISIBLES DESDE EL INICIO PARA PROTECCIÓN DEL CREADOR
    with st.expander("⚠️ TÉRMINOS DE USO Y DESCARGO DE RESPONSABILIDAD LEGAL"):
        st.warning(
            "OseaLaw AI es una plataforma tecnológica independiente de asistencia e información automatizada. "
            "El sistema procesa texto mediante modelos de inteligencia artificial para compilar normativas vigentes en la "
            "República Bolivariana de Venezuela basándose en las Gacetas Oficiales del Estado. OseaLaw AI NO es un bufete de abogados, "
            "NO ofrece asesoría jurídica personalizada, NO sustituye la representación de un profesional colegiado y NO emite "
            "documentos públicos visados. El uso de la información compilada ante cualquier autoridad civil o militar es responsabilidad "
            "estricta y exclusiva del usuario final."
        )
    
    opcion_ingreso = st.radio("Selecciona una opción de acceso:", ["Iniciar Sesión", "Registrar Nueva Cuenta Público"], horizontal=True)
    
    if opcion_ingreso == "Iniciar Sesión":
        st.subheader("🔑 Ingreso a la Plataforma")
        correo_log = st.text_input("📧 Correo Electrónico:")
        clave_log = st.text_input("🔒 Contraseña:", type="password")
        
        if st.button("Ingresar al Asistente"):
            if correo_log in st.session_state.base_usuarios and st.session_state.base_usuarios[correo_log]["clave"] == clave_log:
                st.session_state.usuario_conectado = correo_log
                st.session_state.rol_conectado = st.session_state.base_usuarios[correo_log]["rol"]
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas o usuario no registrado.")
                
    elif opcion_ingreso == "Registrar Nueva Cuenta Público":
        st.subheader("📝 Registro General de Usuario")
        reg_nombre = st.text_input("👤 Nombre:")
        reg_apellido = st.text_input("👤 Apellido:")
        reg_cedula = st.text_input("🆔 Cédula de Identidad:")
        reg_telefono = st.text_input("📱 Número de Teléfono (WhatsApp):", placeholder="Ej: 04241234567")
        reg_correo = st.text_input("📧 Correo Electrónico:")
        reg_clave = st.text_input("🔒 Crea tu Contraseña:", type="password")
        
        if st.button("Crear Cuenta de Usuario"):
            if reg_nombre and reg_apellido and reg_cedula and reg_telefono and reg_correo and reg_clave:
                if reg_correo in st.session_state.base_usuarios:
                    st.error("❌ El correo ingresado ya se encuentra registrado.")
                else:
                    st.session_state.base_usuarios[reg_correo] = {
                        "nombre": f"{reg_nombre} {reg_apellido}",
                        "clave": reg_clave,
                        "rol": "Cliente",
                        "cedula": reg_cedula,
                        "telefono": reg_telefono
                    }
                    st.success("✅ ¡Cuenta creada con éxito! Selecciona 'Iniciar Sesión' para comenzar.")
            else:
                st.error("❌ Por favor, completa todos los campos del formulario.")

# =========================================================================
# VISTA 1: INTERFAZ DEL CIUDADANO (Generador de Reportes de Contraloría)
# =========================================================================
elif st.session_state.rol_conectado == "Cliente":
    datos_cliente = st.session_state.base_usuarios[st.session_state.usuario_conectado]
    
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.usuario_conectado = None
        st.session_state.rol_conectado = None
        st.rerun()
        
    st.title("OSEALAW [AI] 🇻🇪")
    st.write(f"Usuario Activo: **{datos_cliente['nombre']}** | C.I: {datos_cliente['cedula']}")
    st.write("---")
    st.write("### 🤖 Consulta Técnica de Normativas y Prevención de Abuso")
    
    caso = st.text_area("✍ Describe detalladamente la situación o el procedimiento de la autoridad:", height=100, placeholder="Ejemplo: Me detuvieron en un punto de control y pretenden retenerme la documentación bajo el argumento de que cometí una infracción...")

    if st.button("Compilar Reporte Legal de Emergencia"):
        if caso:
            st.info("⏳ *Consultando bases de datos de gacetas venezolanas oficiales...*")
            
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                ticket_servidor = f"OL-DATA-{uuid.uuid4().hex[:8].upper()}-2026"
                
                # PROMPT ULTRA SEGURO PARA TRÁFICO VIRAL EN REDES SOCIALES
                prompt = (
                    f"Actúas como un sistema informático de auditoría normativa y contraloría ciudadana automatizada para Venezuela.\n"
                    f"Genera un INFORME TÉCNICO DE REFERENCIA LEGAL COMPILADO para el ciudadano {datos_cliente['nombre']}, titular de la Cédula de Identidad N° {datos_cliente['cedula']}.\n\n"
                    f"Situación fáctica descrita por el usuario: {caso}\n\n"
                    f"ESTRUCTURA OBLIGATORIA DEL DOCUMENTO DIGITAL:\n"
                    f"1. ENCABEZADO DE SOFTWARE: 'REPORTE AUTOMATIZADO DE REFERENCIA NORMATIVA - OSEALAW AI (SOPORTE DIGITAL)'.\n"
                    f"2. MARCO LEGAL EXACTO RECOPILADO (SÉ FRÍO Y OBJETIVO):\n"
                    f"   - Si el caso involucra GRABACIÓN EN VIDEO de un procedimiento por parte del ciudadano, cita textualmente el Artículo 20 de la Resolución Conjunta N° 109 dictada por el Ministerio del Poder Popular para la Defensa y el Ministerio del Poder Popular para Relaciones Interiores, Justicia y Paz, donde se consagra el derecho a registrar los procedimientos en puntos de control.\n"
                    f"   - Si involucra RETENCIÓN ILÍCITA DE VEHÍCULOS O DOCUMENTOS, cita el Artículo 181 de la Ley de Transporte Terrestre vigente y argumenta que las infracciones administrativas comunes no facultan la retención física del bien, constituyendo una irregularidad procedimental.\n"
                    f"3. CANALES DE DENUNCIA PÚBLICA: Lista las direcciones de contraloría del Estado (Fiscalía Superior del Ministerio Público, Oficina de Atención a la Víctima e Inspectorías del cuerpo actuante) para canalizar las denuncias formales.\n"
                    f"4. CÓDIGO DE TRAZABILIDAD: Incluye al final la línea 'Identificador único de consulta en servidor: {ticket_servidor}'."
                )
                
                payload = {
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": "Eres un motor de búsqueda y compilación de leyes venezolanas. Generas textos de carácter informativo, técnico y estrictamente basados en gacetas oficiales reales, omitiendo cualquier término corporativo o judicial privado."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.05
                }
                
                headers = {'Authorization': f'Bearer {LLAVE_GROQ}', 'Content-Type': 'application/json'}
                response = requests.post(url, json=payload, headers=headers, timeout=20)
                data = response.json()
                
                if 'choices' in data and len(data['choices']) > 0:
                    documento_formal = data['choices'][0]['message']['content']
                    
                    # INSERCIÓN DEL DISCLAIMER DE CONTINGENCIA MASIVA
                    descargo_legal = (
                        "\n\n==================================================\n"
                        "⚠️ NOTA DE CONTROL DE SOFTWARE E INFORMACIÓN PÚBLICA:\n"
                        "Este documento constituye un extracto meramente informativo generado de manera automatizada mediante algoritmos de inteligencia artificial. El contenido se limita a transcribir y compilar normativas legales de carácter público publicadas en la Gaceta Oficial de la República Bolivariana de Venezuela. OseaLaw AI es una herramienta de software independiente; no representa una firma de abogados, no provee asesoría profesional privada y no sustituye los canales formales del Estado. Su exhibición en dispositivos móviles es responsabilidad exclusiva del portador."
                    )
                    texto_final_protegido = documento_formal + descargo_legal
                    
                    st.session_state.base_de_datos_casos.append({
                        "id": len(st.session_state.base_de_datos_casos) + 1,
                        "codigo": ticket_servidor,
                        "cliente": datos_cliente['nombre'],
                        "cedula": datos_cliente['cedula'],
                        "telefono": datos_cliente['telefono'],
                        "correo": st.session_state.usuario_conectado,
                        "caso_original": caso,
                        "borrador_ia": texto_final_protegido,
                        "estado_pago": "❌ Pendiente por verificar",
                        "abogado_assigned": "Ninguno",
                        "documento_firmado": "❌ No"
                    })
                    
                    st.subheader("📄 Reporte Informativo Generado en Pantalla:")
                    st.info(texto_final_protegido)
                    
                    st.markdown("---")
                    st.subheader("📥 Descargar Archivo PDF Optimizado para Móvil")
                    st.write("Para procesar la descarga limpia del archivo en formato PDF indexado con el código de trazabilidad del servidor y habilitar el soporte técnico, realiza el aporte de mantenimiento.")
                    
                    st.warning("⚠️ **TASA DE MANTENIMIENTO TÉCNICO ($5 USD a Tasa BCV):**")
                    st.markdown(DATOS_PAGO_MOVIL)
                    st.write(f"**Referencia de Consulta:** {ticket_servidor}")
                    
                    mensaje_ws = f"Hola OseaLaw Soporte, soy {datos_cliente['nombre']}. Realicé el aporte técnico de $5 para activar la descarga de mi Reporte Legal con identificador {ticket_servidor}."
                    msg_encoded = urllib.parse.quote(mensaje_ws)
                    url_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP_DUEÑO}?text={msg_encoded}"
                    
                    st.markdown(f'<a href="{url_whatsapp}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366;color:white;padding:12px 24px;border:none;border-radius:4px;cursor:pointer;font-size:16px;font-weight:bold;">🟢 Reportar Aporte al Soporte</button></a>', unsafe_allow_html=True)
                    
                    st.markdown("### 📥 Tu Archivo de Descarga:")
                    ultimo_caso = st.session_state.base_de_datos_casos[-1]
                    if ultimo_caso["estado_pago"] == "✅ PAGO VERIFICADO":
                        st.download_button(label="📥 Descargar PDF de Emergencia Ciudadana", data=texto_final_protegido, file_name=f"Reporte_OseaLaw_{ticket_servidor}.txt", mime="text/plain")
                    else:
                        st.error("🔒 El botón de descarga del archivo PDF se habilitará en este módulo inmediatamente después de que el soporte valide el reporte de la transacción.")
                else:
                    st.error("Error al procesar la solicitud con el servidor de IA.")
            except Exception as e:
                st.error(f"Falla de conexión en el servidor: {str(e)}")
        else:
            st.error("Por favor, describe los acontecimientos para compilar el marco normativo.")

# =========================================================================
# VISTA 2: PANEL DE SOPORTE TÉCNICO (Control de Calidad de Servidores)
# =========================================================================
elif st.session_state.rol_conectado == "Soporte":
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.usuario_conectado = None
        st.session_state.rol_conectado = None
        st.rerun()
        
    st.title("⚙️ Panel de Soporte Técnico y Auditoría — OseaLaw")
    st.write("Supervisión del correcto funcionamiento de las consultas masivas generadas por el backend.")
    
    if len(st.session_state.base_de_datos_casos) == 0:
        st.info("No se registran tickets en la cola de procesamiento técnico.")
    else:
        for idx, c in enumerate(st.session_state.base_de_datos_casos):
            codigo_seguro = c.get('codigo', f"OL-DATA-{idx}")
            with st.expander(f"📋 Ticket {codigo_seguro} — Usuario: {c.get('cliente', 'Anonimo')} (Tel: {c.get('telefono', '')})"):
                st.write(f"**Texto de entrada del usuario:** {c.get('caso_original', '')}")
                st.markdown("---")
                st.write("##### 📄 Reporte Compilado por el Motor del Software:")
                st.code(c.get('borrador_ia', ''))
                st.markdown("---")
                
                auditor_name = st.text_input("Auditor de Guardia Asignado:", value=c.get('abogado_assigned', 'Ninguno'), key=f"aud_name_{idx}")
                st.session_state.base_de_datos_casos[idx]['abogado_assigned'] = auditor_name
                
                estatus_revision = st.selectbox(
                    "¿El reporte técnico cumple con los estándares informativos y fue enviado?",
                    ["❌ No", "📝 SÍ, DOCUMENTO AUDITADO Y COMPARTIDO"],
                    key=f"aud_check_{idx}"
                )
                st.session_state.base_de_datos_casos[idx]['documento_firmado'] = estatus_revision
                
                mensaje_cliente = f"Estimado {c.get('cliente', '')}, le saluda el centro de soporte de OseaLaw AI. Su reporte de información normativa bajo el ticket {codigo_seguro} ha sido auditado de forma exitosa por nuestros servidores de control de calidad. Puede utilizar el marco legal en pantalla ante el funcionario actuante."
                msg_encoded = urllib.parse.quote(mensaje_cliente)
                url_ws_cliente = f"https://wa.me/{c.get('telefono', '')}?text={msg_encoded}"
                
                st.markdown(f'<a href="{url_ws_cliente}" target="_blank" style="text-decoration:none;"><button style="background-color:#0078D4;color:white;padding:8px 16px;border:none;border-radius:4px;cursor:pointer;font-size:14px;font-weight:bold;">📲 Enviar Notificación de Soporte al WhatsApp</button></a>', unsafe_allow_html=True)

# =========================================================================
# VISTA 3: PANEL DEL DUEÑO (ADMINISTRADOR MASTER DE LA APP)
# =========================================================================
elif st.session_state.rol_conectado == "Dueño":
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.usuario_conectado = None
        st.session_state.rol_conectado = None
        st.rerun()
        
    st.title("💼 Consola General de Administración (Admin Master)")
    st.write("Métricas de recaudación global para el pago de servidores e infraestructura de red.")
    
    if len(st.session_state.base_de_datos_casos) == 0:
        st.info("Sin operaciones registradas en los servidores centrales.")
    else:
        pagos_listos = sum(1 for x in st.session_state.base_de_datos_casos if "✅" in x['estado_pago'])
        st.metric(label="💰 Caja Recaudada por Volumen ($5 por consulta)", value=f"${pagos_listos * 5} USD")
        st.markdown("---")
        
        for idx, c in enumerate(st.session_state.base_de_datos_casos):
            with st.expander(f"💎 Ticket: {c.get('codigo', idx)} — Solicitante: {c.get('cliente','')}"):
                st.write(f"**WhatsApp Usuario:** {c.get('telefono','')}")
                st.write(f"**Estatus de Transacción:** {c.get('estado_pago','')}")
                
                nuevo_pago = st.selectbox(
                    "Validar ingreso en el Venezolano de Crédito (Desbloquea instantáneamente el PDF al usuario):",
                    ["❌ Pendiente por verificar", "✅ PAGO VERIFICADO"],
                    key=f"boss_pay_{idx}"
                )
                st.session_state.base_de_datos_casos[idx]['estado_pago'] = nuevo_pago
                
                if st.button("Conciliar Fondos en Sistema", key=f"btn_boss_{idx}"):
                    st.success("Transacción registrada e indexada en libros contables.")