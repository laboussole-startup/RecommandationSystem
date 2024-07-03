from datetime import datetime, timedelta
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from users.routes import router as guest_router, user_router
from recommendation.routes import router_recommandation, router_recommandation_metiers, router_recommandation_formation,router_recommandation_formation_populaire
from auth.rooute import router as auth_router
from model_orientation.routes import router_orientation
from starlette.middleware.authentication import AuthenticationMiddleware
from core.security import JWTAuth
#from recommendation.load_data import fetch_data_and_save_to_df  # Assurez-vous que fetch_data_and_save_to_df est correctement importé

app = FastAPI()

# Ajouter CORS Middleware pour permettre les requêtes depuis différentes origines
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplacez par ["http://localhost:3000"] ou les origines spécifiques si nécessaire
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ajouter les routes
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(router_recommandation)
app.include_router(router_orientation)
app.include_router(router_recommandation_formation)
app.include_router(router_recommandation_metiers)
app.include_router(router_recommandation_formation_populaire)

# Ajouter Middleware pour l'authentification
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

@app.get('/')
def health_check():
    return JSONResponse(content={"status": "Running!"})


