from  dotenv import load_dotenv
import os

load_dotenv()



def get_gmail_user():
    gmail_user = os.getenv("GMAIL_USER")
    if(gmail_user):
        return gmail_user
    else:
        raise ValueError("FATAL: La variable de entorno 'GMAIL_USER' es obligatoria y no está configurada. Revisa tu archivo .env.")
    
def get_gmail_app_password():
    pass_app_user = os.getenv("GMAIL_PASS_APP")
    if(pass_app_user):
        return pass_app_user
    else:
        raise ValueError("FATAL: La variable de entorno 'GMAIL_PASS_APP' es obligatoria y no está configurada. Revisa tu archivo .env.")

    

