from typing import List
from fastapi import APIRouter, HTTPException, Query
from recommendation.sr_faculte import faculty_recommendation
from recommendation.recommandationMetiers import metiers_recommandations
from recommendation.sr_formation import formations_recommandation
from recommendation.systeme_de_recommandation import formations_recommandation_populaire


router_recommandation = APIRouter(
    prefix="/recommandation_faculté",
    tags=["Recommandation_faculté"],
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
    Route pour obtenir des recommandations des formation.
    """
    # Appel de la fonction de recommandation avec les paramètres fournis
    recommended_courses = faculty_recommendation(
        centre_interet,
        pays_user,
        historique_recherche,
        user_diplome,
        page=page,
        page_size=page_size
    )
    
    # Retourner les recommandations sous forme de dictionnaire
    return {"recommendations": recommended_courses}


#recommandation formation
router_recommandation_formation = APIRouter(
    prefix="/recommendation_formation",
    tags=["recommendation_formation"],
    responses={404: {"description": "Not found"}},
    #dependencies=[Depends(oauth2_scheme)]
)

@router_recommandation_formation.get("/")
def get_recommendations(
    centre_interet: List[str] = Query(None),  # Paramètre optionnel pour les centres d'intérêt de l'utilisateur
    pays_user: str = Query(None),  # Paramètre obligatoire pour le pays de l'utilisateur
    user_diplome: List[str] = Query(None),  # Paramètre optionnel pour les diplômes de l'utilisateur
    historique_recherche: List[str] = Query(None),  # Paramètre optionnel pour l'historique de recherche de l'utilisateur
    page: int = 1,  # Paramètre optionnel pour le numéro de la page de résultats, valeur par défaut 1
    page_size: int = 10  # Paramètre optionnel pour la taille de la page de résultats, valeur par défaut 10
):
    """
    Route pour obtenir des recommandations de formation.
    """
    # Appel de la fonction de recommandation avec les paramètres fournis
    recommended_courses = formations_recommandation(
        centre_interet,
        pays_user,
        historique_recherche,
        user_diplome,
        page=page,
        page_size=page_size
    )
    
    # Retourner les recommandations sous forme de dictionnaire
    return {"recommendations": recommended_courses}


#recommandation metier
router_recommandation_metiers = APIRouter(
    prefix="/metiers_recommandations",
    tags=["metiers_recommandations"],
    responses={404: {"description": "Not found"}},
    #dependencies=[Depends(oauth2_scheme)]
)

@router_recommandation_metiers.get("/")
def get_recommendations(
    centre_interet: List[str] = Query(None),  # Paramètre optionnel pour les centres d'intérêt de l'utilisateur
    user_competence: List[str]=Query(None),
    pays_user: str = Query(None),  # Paramètre obligatoire pour le pays de l'utilisateur
    user_diplome: List[str] = Query(None),  # Paramètre optionnel pour les diplômes de l'utilisateur
    historique_recherche: List[str] = Query(None),  # Paramètre optionnel pour l'historique de recherche de l'utilisateur
    competence:List[str] = Query(None),
    page: int = 1,  # Paramètre optionnel pour le numéro de la page de résultats, valeur par défaut 1
    page_size: int = 10  # Paramètre optionnel pour la taille de la page de résultats, valeur par défaut 10
):
    """
    Route pour obtenir des recommandations de formation.
    """
    # Appel de la fonction de recommandation avec les paramètres fournis
    recommended_courses = metiers_recommandations(
        centre_interet,
        user_competence,
        user_diplome,
        page=page,
        page_size=page_size,
        
        
    )
    
    # Retourner les recommandations sous forme de dictionnaire
    return {"recommendations": recommended_courses}



#formation populaire
router_recommandation_formation_populaire = APIRouter(
    prefix="/recommend_formation_populaire",
    tags=["recommend_formation_populaire"],
    responses={404: {"description": "Not found"}},
    #dependencies=[Depends(oauth2_scheme)]
)

@router_recommandation_formation_populaire.get("/")
def get_recommendations(
    page: int = 1,  # Paramètre optionnel pour le numéro de la page de résultats, valeur par défaut 1
    page_size: int = 10  # Paramètre optionnel pour la taille de la page de résultats, valeur par défaut 10
):
    """
    Route pour obtenir des recommandations de métiers.
    """
    try:
        # Appel de la fonction de recommandation avec les paramètres fournis
        recommended_metiers = formations_recommandation_populaire(
            page=page,
            page_size=page_size
        )
        
        # Retourner les recommandations sous forme de dictionnaire
        return {"recommendations": recommended_metiers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération des recommandations : {e}")
