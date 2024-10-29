import paho.mqtt.client as paho
import time
import streamlit as st
import json

# Variables iniciales
values = 0.0
act1 = "OFF"
message_received = ""

# Configuración de MQTT
broker = "broker.mqttdashboard.com"
port = 1883

# Funciones para el cliente MQTT
def on_publish(client, userdata, result):  
    st.success("✅ Dato publicado con éxito")
    pass

def on_message(client, userdata, message):
    global message_received
    message_received = str(message.payload.decode("utf-8"))
    st.write(f"📩 Mensaje recibido: {message_received}")

client1 = paho.Client("cliente_mqtt_control")
client1.on_publish = on_publish
client1.on_message = on_message
client1.connect(broker, port)

# Interfaz en Streamlit
st.set_page_config(page_title="Control MQTT", page_icon="🚀")
st.title("🚀 Control de Actuadores y Envío de Datos con MQTT")

# Indicadores de estado y botones
st.sidebar.header("📊 Estado del Actuador")
actuator_status = st.sidebar.empty()

if st.button('🔴 Encender Actuador'):
    act1 = "ON"
    message = json.dumps({"Act1": act1})
    client1.publish("mpjr1", message)
    actuator_status.success("Estado: Actuador ENCENDIDO")
else:
    st.write('')

if st.button('🔵 Apagar Actuador'):
    act1 = "OFF"
    message = json.dumps({"Act1": act1})
    client1.publish("mpjr1", message)
    actuator_status.warning("Estado: Actuador APAGADO")
else:
    st.write('')

# Control de valores analógicos
st.header("📟 Enviar Valor Analógico")
values = st.slider('Selecciona un valor de 0 a 100:', 0.0, 100.0)
st.write(f"Valor seleccionado: {values}")

if st.button('📤 Enviar Valor Analógico'):
    message = json.dumps({"Analog": float(values)})
    client1.publish("mpjr2", message)
    st.info("🔄 Enviando valor analógico...")
else:
    st.write('')

# Mensajes recibidos en tiempo real
st.header("📬 Mensajes Recibidos")
if message_received:
    st.write(f"Mensaje MQTT recibido: {message_received}")
else:
    st.info("🔍 Esperando mensajes...")

# Mantener suscripción activa
client1.loop_start()
