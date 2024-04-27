import json
from fastapi import FastAPI, Body, HTTPException
import xmlrpc.client
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List


app = FastAPI()
app.title = "App MOBI"
app.version = "2.0.0"

# Datos de conexion
url = 'http://localhost:8069'
db = 'mobi_prd_test_af_api'
username = 'soporte'
password = 'S0portE123!*'

# producto_name producto_id _lote_id contacto_id, location_id, date,

class product_assignment(BaseModel):
    lot_id: str
    partner_id: str
    location_id: str
    date: str

class User(BaseModel):
        cod_app: int
        name: str 
        vat: str
        phone: str 
        mobile: str
        email: str 
        street: str
        street2: str 
        zip: str 
        city: str
        state_name: str 
        country: str 
        stage_key: str 
        payment_date: str
        payment_state: str 
        payment_amount: int




@app.get('/', tags=['Home'])
def home():
    return "Hola mundo"

@app.get('/home', tags=['Home'])
def home():
    return "Hola mundo"

# Definición de la ruta para recibir datos y enviarlos a Odoo
@app.post('/cliente', tags=['Cliente'])
def send_user(user: User):
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {}) 
        # Ejecutamos nuestro "EndPoint /xmlrpc/2/object" devolviendo un objeto que utilizamos para ejecutar una instruccion en Odoo 16 
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        
        json_data = user.__dict__
        
        # Llamar al método en Odoo para procesar los datos JSON
        resultado = models.execute_kw(db, uid, password,'crm.lead', 'process_json_data', [json_data])
        add_row_user_payment = ''
        if resultado == "1":
            add_row_user_payment = {
                "code": resultado,
                "message": "No se encontro la ubicación de la reserva",
            }
        else:
            add_row_user_payment = {
                "code": resultado,
                "message": "JSON recibido correctamente",
            }
        print("Respuesta de Odoo: ", resultado)
        return add_row_user_payment
    
    except Exception as e:
        # Si hay algún error, devolver un error HTTP 500
        raise HTTPException(status_code=500, detail=str(e))
        

@app.post('/send_products/')
async def send_products(items: List[product_assignment]):
    try:
        registros_procesados = []
        for item in items:
             registros_procesados.append({
           'lot_id': item.lot_id,
           'partner_id': item.partner_id,
            'location_id': item.location_id,
            'date': item.date,
        })     
        print(registros_procesados)
        
        return {"code": "0",
                "message": "JSON recibido correctamente",
                "data": registros_procesados}
    except Exception as e:
        # Si hay algún error al procesar el JSON, lanzamos una excepción HTTP 422
        raise HTTPException(status_code=422, detail=str(e))
