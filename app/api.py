from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv

import routeros_api
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

app = FastAPI()

# Configuración CORS
origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
@app.post("/preview")
async def preview(request: Request):
    data = await request.json()
    IP_MIKROTIK = data.get('IP_MIKROTIK')
    SPREADSHEET_NAME = data.get('SPREADSHEET_NAME')
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    load_dotenv()
    KEY = os.getenv('KEY')
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
    PASS_MIKROTIK = os.getenv('PASS_MIKROTIK')
    USER_MIKROTIK = os.getenv('USER_MIKROTIK')

    # ==============================================================================
    # conexion a google sheets
    creds = None
    creds = service_account.Credentials.from_service_account_file(KEY,scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # obteniendo los valores
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SPREADSHEET_NAME).execute()

    values = result.get('values', [])
    DATA_PARSED = []
    # Obtén los encabezados de la hoja de cálculo
    headers = values[0]

    # Convierte cada fila de la hoja de cálculo en un diccionario
    for row in values[1:]:
        data = {}
        for i in range(len(headers)):
            data[headers[i]] = row[i]
        DATA_PARSED.append(data)

    # creamos sheet_list
    sheet_list = []
    for client in DATA_PARSED:
        sheet_data = {'ip' : client["ip"], 'nombre' : client['nombre']}
        sheet_list.append(sheet_data)

    # conexion con la api Miktoik
    connection = routeros_api.RouterOsApiPool(IP_MIKROTIK, username=USER_MIKROTIK, password=PASS_MIKROTIK, plaintext_login=True)
    api = connection.get_api()

    # obtengo el address list de la lista 'Suspendido'
    response = api.get_resource("/ip/firewall/address-list").get(list='Suspendido')
    addr_list = []
    susp_list = []
    # si no esta en addr_list lo agregamos
    for ip in response:
        addr_list.append({'ip' : ip['address'],'comment' : ip['comment']})    # ips mkt

    for item in addr_list:
        if item in sheet_list:
            susp_list.append(item)
            
    addr_list_ip = []
    for ip in addr_list:
        addr_list_ip.append(ip['ip'])

    for item in sheet_list:
            if item['ip'] not in addr_list_ip:
                created_client = api.get_resource("/ip/firewall/address-list").add(address = item['ip'], list = 'Suspendido', comment = item['nombre'])
    response = api.get_resource("/ip/firewall/address-list").get(list='Suspendido')
    
    addr_list_updated = []
    for ip in response:
        addr_list_updated.append({'ip' : ip['address'],'comment' : ip['comment']})    # ips mkt
    
    addr_list_updated_in_sheets = []
    for i in addr_list_updated:
        for e in sheet_list:
            if i['ip'] == e['ip']:
                item = {'ip' : i['ip'], 'comment' : i['comment']}
                addr_list_updated_in_sheets.append(item)

    comment_list = []
    for comment in addr_list:
        for item in sheet_list:
            if item['ip'] == comment['ip']:
                item = {'ip' : comment['ip'], 'comment' : comment['comment']}
                comment_list.append(item)   # lista de comentarios

    fecha = ' // SUSPENDIDO - 09/05/2023'
    comment_finally = []
    for com in addr_list_updated_in_sheets:
        item =  {'ip':com['ip'], 'comment':com['comment'] + fecha}
        comment_finally.append(item)

    return [comment_list, comment_finally]


@app.post("/script")
async def main(request: Request):
    data = await request.json()
    IP_MIKROTIK = data.get('IP_MIKROTIK')
    SPREADSHEET_NAME = data.get('SPREADSHEET_NAME')
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # Cargar variables de entorno del archivo .env
    load_dotenv()
    KEY = os.getenv('KEY')
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
    PASS_MIKROTIK = os.getenv('PASS_MIKROTIK')
    USER_MIKROTIK = os.getenv('USER_MIKROTIK')

    # conexion a google sheets
    creds = None
    creds = service_account.Credentials.from_service_account_file(KEY,scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # obteniendo los valores
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SPREADSHEET_NAME).execute()

    values = result.get('values', [])
    DATA_PARSED = []
    # Obtén los encabezados de la hoja de cálculo
    headers = values[0]

    # Convierte cada fila de la hoja de cálculo en un diccionario
    for row in values[1:]:
        data = {}
        for i in range(len(headers)):
            data[headers[i]] = row[i]
        DATA_PARSED.append(data)

    # creamos sheet_list
    sheet_list = []
    for client in DATA_PARSED:
        sheet_data = {'ip' : client["ip"], 'nombre' : client['nombre']}
        sheet_list.append(sheet_data)

    # ==============================================================================

    # conexion con la api Miktoik
    connection = routeros_api.RouterOsApiPool(IP_MIKROTIK, username=USER_MIKROTIK, password=PASS_MIKROTIK, plaintext_login=True)
    api = connection.get_api()

    # obtengo el address list de la lista 'Suspendido'
    response = api.get_resource("/ip/firewall/address-list").get(list='Suspendido')
    addr_list = []
    for ip in response:
        addr_list.append(ip['address'])    # ips mkt

    # si no esta en addr_list lo agregamos
    for item in sheet_list:
        if item['ip'] not in addr_list:
            created_client = api.get_resource("/ip/firewall/address-list").add(address = item['ip'], list = 'Suspendido', comment = item['nombre'])
            response = api.get_resource("/ip/firewall/address-list").get(list='Suspendido')

    # recorro response para generar una lista que solo contenga el id + la ip + comentario (lista de suspendidos)
    susp_list = []
    for id in response:
        if id in response:
            item = ({'id' : id['id'],'address' : id['address'], 'comment' : id['comment']})
            susp_list.append(item)    # id + ip a suspender

    # recorro susp_list para generar la lista de suspension que contiene solamente los id de las ip que coinciden con addr_list
    susp_list_id = []
    for ip in sheet_list:
        for item in susp_list:
            if item['address'] == ip['ip']:
                # Si el nombre coincide, agregar el diccionario a la lista susp_list_id
                susp_list_id.append(item['id'])  # lista de los ids a suspender

    comment_list = []
    for comment in susp_list:
        for item in sheet_list:
            if item['ip'] == comment['address']:
                item = {'id' : comment['id'], 'comment' : comment['comment']}
                comment_list.append(item)   # lista de comentarios

    fecha = ' // SUSPENDIDO - 09/05/2023'
    comment_finally = []
    for com in comment_list:
        item =  {'id':com['id'], 'comment':com['comment'] + fecha}
        comment_finally.append(item)

    # recorro susp_list_id para ejecutar la accion de suspender en mikrotik en cada iteracion
    for id_suspense in susp_list_id:
        id_suspense_list = api.get_resource("/ip/firewall/address-list").set(id = id_suspense, disabled = 'false') # lista que se suspendio (accion ejecutada)

    # recorro comment_list para ejecutar la accion de editar el comentario en mikrotik en cada iteracion
    for comment_suspense in comment_finally:
        comment_suspense_list = api.get_resource("/ip/firewall/address-list").set(id = comment_suspense['id'], comment = comment_suspense['comment'])

    # me desconecto de la api
    connection.disconnect()

    return {'message': 'done'}


