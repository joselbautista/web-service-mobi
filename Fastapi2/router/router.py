from fastapi import FastAPI, APIRouter, Response, Body ,HTTPException
import xmlrpc.client
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.customer import Customer
from schema.customer import CustomersList
from schema.assigment import product_assignment
from models.connection import OdooConnection
from typing import List
#from werkzeug.security import generate_password_hash, check_password_hash

router = APIRouter()
conn = OdooConnection()

@router.get('/', tags=['Home'])
def home():
    return "Hola mundo"

@router.get('/home', tags=['Home'])
def home():
    return "Hola mundo"

# Definición de la ruta para recibir datos y enviarlos a Odoo
@router.post('/customers', tags=['Customer'])
def send_user(customers: List[Customer]):
    try:
        print(customers)
        customers_dict = [customer.dict() for customer in customers]
        add_row_user_payment = ''
        resultado = conn.get_customer(customers_dict)
    
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
        

@router.post('/send_products/')
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
        return {"code": "0",
                "message": "JSON recibido correctamente",
                "data": registros_procesados}
    except Exception as e:
        # Si hay algún error al procesar el JSON, lanzamos una excepción HTTP 422
        raise HTTPException(status_code=422, detail=str(e))
