from typing import List
from fastapi import APIRouter, HTTPException, Query
from recommendation.sr import recommend_courses
from recommendation.recommandationMetiers import recommend_metiers


router_recommandation = APIRouter(
    prefix="/recommend",
    tags=["Recommend"],
    responses={404: {"description": "Not found"}},
    #dependencies=[Depends(oauth2_scheme)]
)


@router_recommandation.get("/")
def get_recommendations(
    centre_interet: List[str] = Query(None),  # Paramètre optionnel pour les centres d'intérêt de l'utilisateur
    pays_user: str = Query(None),  # Paramètre obligatoire pour le pays de l'utilisateur
    user_diplome: List[str] = Query(None),  # Paramètre optionnel pour les diplômes de l'utilisateur
    historique_recherche: List[str] = Query(None),  # Paramètre optionnel pour l'historique de recherche de l'utilisateur
    page: int = 1,  # Paramètre optionnel pour le numéro de la page de résultats, valeur par défaut 1
    page_size: int = 10  # Paramètre optionnel pour la taille de la page de résultats, valeur par défaut 10
):
    """
    Route pour obtenir des recommandations de cours.
    """
    # Appel de la fonction de recommandation avec les paramètres fournis
    recommended_courses = recommend_courses(
        centre_interet,
        pays_user,
        historique_recherche,
        user_diplome,
        page=page,
        page_size=page_size
    )
    
    # Retourner les recommandations sous forme de dictionnaire
    return {"recommendations": recommended_courses}


router_recommandation_metiers = APIRouter(
    prefix="/recommend_metiers",
    tags=["recommend_metiers"],
    responses={404: {"description": "Not found"}},
    #dependencies=[Depends(oauth2_scheme)]
)

@router_recommandation_metiers.get("/")
def get_recommendations(
    centre_interet: List[str] = Query(None),  # Paramètre optionnel pour les centres d'intérêt de l'utilisateur
    user_competence: List[str] = Query(None),  # Paramètre optionnel pour les compétences de l'utilisateur
    historique_recherche: List[str] = Query(None),  # Paramètre optionnel pour l'historique de recherche de l'utilisateur
    page: int = 1,  # Paramètre optionnel pour le numéro de la page de résultats, valeur par défaut 1
    page_size: int = 10  # Paramètre optionnel pour la taille de la page de résultats, valeur par défaut 10
):
    """
    Route pour obtenir des recommandations de métiers.
    """
    try:
        # Appel de la fonction de recommandation avec les paramètres fournis
        recommended_metiers = recommend_metiers(
            centre_interet,
            user_competence,
            historique_recherche,
            page=page,
            page_size=page_size
        )
        
        # Retourner les recommandations sous forme de dictionnaire
        return {"recommendations": recommended_metiers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération des recommandations : {e}")
