from fastapi import HTTPException
import xmlrpc.client
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Accede a las variables de entorno
con_url = os.getenv("CON_URL")
con_db = os.getenv("CON_DB")
con_username = os.getenv("CON_USERNAME")
con_password = os.getenv("CON_PASSWORD")

class OdooConnection():
    def get_customer(self, customer):
        try:
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(con_url))
            uid = common.authenticate(con_db, con_username, con_password, {}) 
            # Ejecutamos nuestro "EndPoint /xmlrpc/2/object" devolviendo un objeto que utilizamos para ejecutar una instruccion en Odoo 16 
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(con_url))
            
            json_data = customer
            #json_data = customer.__dict__
            #print(json_data)
            
            # Llamar al método en Odoo para procesar los datos JSON
            resultado = models.execute_kw(con_db, uid, con_password,'crm.lead', 'process_json_data', [json_data])
            return resultado
        except Exception as e:
            # Si hay algún error, devolver un error HTTP 500
            raise HTTPException(status_code=500, detail=str(e))