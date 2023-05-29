from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.routes import router 

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
# Rutas
app.include_router(router)
