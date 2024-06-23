from typing import List
from fastapi import APIRouter, Query
from recommendation.sr import recommend_courses
from recommendation.recommandationMetiers import recommend_metiers


router_recommandation = APIRouter(
    prefix="/recommend",
    tags=["Recommend"],
    responses={404: {"description": "Not found"}},
    #dependencies=[Depends(oauth2_scheme)]
)

@router_recommandation.get("/")
def get_recommendations(centre_interet: List[str] = Query(..., min_length=1),pays_user: str = Query(..., min_length=1),user_diplome: list[str]=Query(..., min_length=1), historique_recherche: List[str] = Query(None), page: int = 1, page_size: int = 10):
    recommended_courses = recommend_courses(centre_interet,pays_user,historique_recherche,user_diplome, page=page, page_size=page_size)
    return {"recommendations": recommended_courses}

router_recommandation_metiers = APIRouter(
    prefix="/recommend_metiers",
    tags=["recommend_metiers"],
    responses={404: {"description": "Not found"}},
    #dependencies=[Depends(oauth2_scheme)]
)

@router_recommandation_metiers.get("/")
def get_recommendations_metiers(user_interests: List[str] = Query(...), 
                                user_competence: List[str] = Query(None), 
                                historique_recherche_utilisateur: List[str] = Query(None), 
                                page: int = Query(1), 
                                page_size: int = Query(10)):
    recommendations = recommend_metiers(user_interests, user_competence, historique_recherche_utilisateur, page, page_size)
    return recommendations