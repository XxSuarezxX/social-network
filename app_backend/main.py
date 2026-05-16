from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Importación necesaria
from api.v1.endpoints.user import router as user_router
from api.v1.endpoints.auth import router as auth_router
from api.v1.endpoints.post import router as post_router

app = FastAPI()

# Configuración de Orígenes permitidos
# Aquí defines quién tiene permiso para consumir tu API
origins = [
    "http://127.0.0.1:8080",  # Dirección estándar de Live Server
    "http://localhost:8080",
    "http://127.0.0.1:5500"
]

# Agregamos el middleware a la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los headers (Content-Type, Authorization, etc.)
)

# Registro de Routers
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(post_router)