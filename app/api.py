from fastapi import FastAPI
import routeros_api
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()
queues = []
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
#post model
class Data(BaseModel):
    ip_mkt: Optional[str]
    usuario: Optional[str]
    passwords: Optional[str]
    id_sheet: Optional[str]
    name_sheet: Optional[str]
    execute_at: datetime = datetime.now
    
@app.get("/")
def show_queues():
    connection = routeros_api.RouterOsApiPool('192.168.2.238', username='admin', password='test1234', plaintext_login=True)

    api = connection.get_api()
    queueList = []
    getQueueList = api.get_resource('/queue/simple').get()
    for queue in getQueueList:
        queue = {'id': queue['id'],'DirecciónIP': queue['target'],'name': queue['name'],'maxLimit': queue['max-limit'],'burst-limit': queue['burst-limit'],'burst-threshold': queue['burst-threshold']}
        queueList.append(queue)
    connection.disconnect()
    return ('hola')
