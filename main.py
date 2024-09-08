from datetime import datetime, timedelta
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from recommendation.routes import router_recommandation,router_recommandation_formation,router_recommandation_formation_populaire,router_recommandation_metiers
from elearning.models.modelsSQLAlchemy import Base
from core.database import engine
from elearning.api import auth, utilisateur, formation, module, cours, resume, quiz, question, reponse, historique, conference_video,enrollment,gestion_formation_user,create_meet

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplacez par ["http://localhost:3000"] ou les origines spécifiques si nécessaire
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(utilisateur.router, prefix="/utilisateurs", tags=["utilisateurs"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(formation.router, prefix="/formations", tags=["formations"])
app.include_router(module.router, prefix="/modules", tags=["modules"])
app.include_router(cours.router, prefix="/cours", tags=["cours"])
app.include_router(gestion_formation_user.router, prefix="/user_formations_status", tags=["user_formations_status"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
app.include_router(enrollment.router, prefix="/inscription", tags=["inscription"])
#app.include_router(create_meet.router, prefix="/create_meet", tags=["create_meet"])
app.include_router(router_recommandation_formation)
app.include_router(router_recommandation_metiers)
app.include_router(router_recommandation)
app.include_router(router_recommandation_formation_populaire)
# app.include_router(resume.router, prefix="/resumes", tags=["resumes"])
# app.include_router(question.router, prefix="/questions", tags=["questions"])
# app.include_router(reponse.router, prefix="/reponses", tags=["reponses"])
# app.include_router(historique.router, prefix="/historiques", tags=["historiques"])
# app.include_router(conference_video.router, prefix="/conferences", tags=["conferences"])

# Ajouter CORS Middleware pour permettre les requêtes depuis différentes origines

@app.get('/')
def health_check():
    return JSONResponse(content={"status": "Running!"})
