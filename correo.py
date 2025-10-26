import imaplib
import email
from email.header import decode_header
import datetime
import logging

from config import get_gmail_user
from config import get_gmail_app_password


email_user = get_gmail_user()
app_password = get_gmail_app_password()

def get_emails_last_24hours() -> list[dict]:
    conexion = None
    try:
        conexion = imaplib.IMAP4_SSL("imap.gmail.com")
        conexion.login(email_user, app_password)
        
        status_select, _ = conexion.select("INBOX")
        if status_select != "OK":
            raise RuntimeError("No se pudo seleccionar la bandeja INBOX")

        hace_24h = datetime.datetime.now() - datetime.timedelta(hours=24)
        fecha_imap = hace_24h.strftime("%d-%b-%Y")
        
        status, ids_correos = conexion.search(None, f'SINCE "{fecha_imap}"')
        if status != "OK":
            raise RuntimeError(f"Error al buscar correos: {ids_correos}")
            
        lista_ids = ids_correos[0].split()
        correos_procesados = []
        
        for correo_id in lista_ids:
            status, datos_correo = conexion.fetch(correo_id, "(RFC822)")
            if status != "OK":
                print(f"No se pudo obtener el correo {correo_id}")
                continue
                
            raw_email = datos_correo[0][1]
            mensaje = email.message_from_bytes(raw_email)
            
            message_id = mensaje.get("Message-ID", None)
            if message_id is None:
                print("Correo sin Message-ID")
            
            remitente = mensaje.get("From", "")
            
            # Decodificación simple de asunto
            subject_header = mensaje.get("Subject", "")
            try:
                asunto_decoded = decode_header(subject_header)[0]
                asunto = asunto_decoded[0]
                if isinstance(asunto, bytes):
                    asunto = asunto.decode(asunto_decoded[1] or "utf-8", errors="replace")
            except Exception:
                asunto = subject_header  # fallback
            
            fecha_str = mensaje.get("Date", "")
            
            # Extracción de cuerpo (igual que antes)
            cuerpo = ""
            if mensaje.is_multipart():
                for parte in mensaje.walk():
                    if parte.get_content_type() == "text/plain":
                        cuerpo = parte.get_payload(decode=True)
                        break
                if not cuerpo:
                    cuerpo = "[Contenido HTML]"
            else:
                cuerpo = mensaje.get_payload(decode=True)

            if isinstance(cuerpo, bytes):
                cuerpo = cuerpo.decode("utf-8", errors="replace")
                
            correo_limpio = {
                "message_id": message_id,
                "remitente": remitente,
                "asunto": asunto,
                "fecha": fecha_str,
                "cuerpo": cuerpo[:1000]
            }
            correos_procesados.append(correo_limpio)
        
        return correos_procesados  # ✅ ¡Fuera del bucle!
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
    finally:
        if conexion:
            try:
                conexion.logout()
            except:
                pass
            
