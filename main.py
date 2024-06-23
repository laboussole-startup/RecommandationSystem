from datetime import datetime, timedelta
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from users.routes import router as guest_router, user_router
from recommendation.routes import router_recommandation,router_recommandation_metiers
from auth.rooute import router as auth_router 
from model_orientation.routes import router_orientation
from starlette.middleware.authentication import AuthenticationMiddleware
from core.security import JWTAuth
# from recommendation.load_data import fetch_data_and_save_to_csv, get_last_update_time, save_last_update_time  # Importer la fonction fetch_data_and_save_to_csv

app = FastAPI()

app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(router_recommandation)
app.include_router(router_orientation)

app.include_router(router_recommandation_metiers)

# Add Middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

@app.get('/')

def health_check():
    # Appeler fetch_data_and_save_to_csv() au démarrage de l'application
   
    # Charger les données à partir du fichier CSV
    return JSONResponse(content={"status": "Running!"})





