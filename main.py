import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twilio.rest import Client

# 1. Configuración de credenciales de Twilio
twilio_phone_number = 'whatsapp:+14155238886'

account_sid = os.environ.get('account_sid')
auth_token = os.environ.get('au')
if not auth_token or not account_sid:
    try:
        import bridges
        auth_token = auth_token or bridges.au
        account_sid = account_sid or bridges.account_sid
    except ImportError:
        print("Advertencia: No se encontró la variable de entorno 'au'/'account_sid' ni el archivo 'bridges.py'")

# Inicializamos el cliente de Twilio
client = Client(account_sid, auth_token)

app = FastAPI()

# 2. Definimos la estructura de datos que esperamos recibir
class MensajeRequest(BaseModel):
    numero: str
    mensaje: str

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running!"}

# 3. Endpoint principal para enviar mensajes de texto libre
@app.post("/enviar_mensaje")
def enviar_mensaje(req: MensajeRequest):
    try:
        # Asegurarnos de que el número tenga el formato de WhatsApp de Twilio
        numero_destino = req.numero
        # Agregar el código de país si no está presente
        if not numero_destino.startswith("+"):
            numero_destino = f"+52{numero_destino}"
        if not numero_destino.startswith("whatsapp:"):
            numero_destino = f"whatsapp:{numero_destino}"

        # Enviamos el mensaje usando Twilio
        message = client.messages.create(
            from_=twilio_phone_number,
            body=req.mensaje,
            to=numero_destino
        )
        
        return {
            "status": "success", 
            "message_sid": message.sid,
            "info": f"Mensaje enviado a {numero_destino}"
        }
    except Exception as e:
        # Si Twilio marca error (ej. número inválido), regresamos error 500
        raise HTTPException(status_code=500, detail=str(e))
