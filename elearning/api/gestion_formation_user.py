from typing import Dict, List, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_current_user  # Cette fonction doit être définie pour obtenir l'utilisateur actuel
from elearning.models.modelsSQLAlchemy import Formation, Module, Quiz, UserFormationLink, UserModuleLink, UserQuizLink, Utilisateur
from elearning.schemas.SchemasPydantic import FormationRead, ModuleRead, QuizSummaryOut, UtilisateurRead, ValidatedModuleOut, ValidatedQuizOut, FormationStatusOut

router = APIRouter()

# Fonction pour obtenir le statut des formations d'un utilisateur
@router.get("/user/{user_id}/formation-status", response_model=List[FormationStatusOut])
async def get_user_formation_status( db: Session = Depends(get_db), current_user:Utilisateur = Depends(get_current_user)):
    try:
        
        user_formation_links = db.query(UserFormationLink).filter(UserFormationLink.user_id == current_user.id_utilisateur).all()

        if not user_formation_links:
            raise HTTPException(status_code=404, detail="Aucune formation trouvée pour cet utilisateur.")

        formation_status_list = []
        for link in user_formation_links:
            instructeur_data = UtilisateurRead(
                id_utilisateur=link.formation.instructeur.id_utilisateur,
                nom=link.formation.instructeur.nom,
                prenom=link.formation.instructeur.prenom,
                email=link.formation.instructeur.email,
                role=link.formation.instructeur.role,
                est_actif=link.formation.instructeur.est_actif
            )
            
            formation_status_list.append(FormationStatusOut(
                formation=FormationRead(
                    id_formation=link.formation.id_formation,
                    titre=link.formation.titre,
                    description=link.formation.description,
                    url_image_formation=link.formation.url_image_formation,
                    instructeur=instructeur_data
                ),
                in_progress=True  # Exemple de valeur pour in_progress
            ))

        return formation_status_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# # Endpoint pour voir les modules validés et leurs notes pour une formation
# @router.get("/user/formations/{formation_id}/modules/validated/", response_model=List[ValidatedModuleOut])
# def get_validated_modules(formation_id: int, db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)):
#     """
#     Endpoint pour voir les modules validés et leurs notes pour une formation.
#     """
#     modules = db.query(Module).filter(Module.id_formation == formation_id).all()
#     validated_modules = []

#     for module in modules:
#         module_link = db.query(UserModuleLink).filter(UserModuleLink.user_id == current_user.id_utilisateur, UserModuleLink.module_id == module.id_module).first()
#         if module_link:
#             validated_modules.append(ValidatedModuleOut(
#                 module=ModuleRead(
#                     id_module=module.id_module,
#                     titre=module.titre,
#                     description=module.description,
#                     id_formation=module.id_formation
#                 ),
#                 score=module_link.score  # Ajoutez une colonne score dans UserModuleLink si nécessaire
#             ))

#     return validated_modules

# Endpoint pour voir les quiz validés et leurs notes pour un module
@router.get("/user/modules/{module_id}/quizzes/validated/", response_model=List[ValidatedQuizOut])
def get_validated_quizzes(module_id: int, db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)):
    """
    Endpoint pour voir les quiz validés et leurs notes pour un module.
    """
    quizzes = db.query(Quiz).filter(Quiz.id_module == module_id).all()
    validated_quizzes = []

    for quiz in quizzes:
        quiz_link = db.query(UserQuizLink).filter(UserQuizLink.user_id == current_user.id_utilisateur, UserQuizLink.quiz_id == quiz.id_quiz).first()
        if quiz_link:
            validated_quizzes.append(ValidatedQuizOut(
                quiz=QuizSummaryOut(
                    id_quiz=quiz.id_quiz,
                    titre=quiz.titre,
                    score=quiz_link.score,
                    passed=quiz_link.passed
                ),
                score=quiz_link.score
            ))

    return validated_quizzes



@router.get("/user/formations/{formation_id}/modules/validated/", response_model=List[ValidatedModuleOut])
def get_validated_modules(formation_id: int, db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)):
    """
    Endpoint pour voir les modules validés et leurs notes pour une formation.
    """
    modules = db.query(Module).filter(Module.id_formation == formation_id).all()
    validated_modules = []

    for module in modules:
        module_link = db.query(UserModuleLink).filter(UserModuleLink.user_id == current_user.id_utilisateur, UserModuleLink.module_id == module.id_module).first()
        if module_link:
            validated_modules.append(ValidatedModuleOut(
                module=ModuleRead(
                    id_module=module.id_module,
                    titre=module.titre,
                    description=module.description,
                    url_image_module=module.url_image_module,
                    formation=FormationRead(
                        id_formation=module.formation.id_formation,
                        titre=module.formation.titre,
                        description=module.formation.description,
                        url_image_formation=module.formation.url_image_formation,
                        instructeur=UtilisateurRead(
                            id_utilisateur=module.formation.instructeur.id_utilisateur,
                            nom=module.formation.instructeur.nom,
                            prenom=module.formation.instructeur.prenom,
                            email=module.formation.instructeur.email,
                            role=module.formation.instructeur.role,
                            est_actif=module.formation.instructeur.est_actif
                        )
                    )
                ),
                score=module_link.score
            ))

    return validated_modules



@router.get("/formations/{formation_id}/modules/status", response_model=List[Dict[str, Union[ModuleRead, bool]]])
def get_modules_status(formation_id: int, db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)):
    """
    Endpoint pour voir tous les modules d'une formation avec leur statut (validé ou non).
    """
    modules = db.query(Module).filter(Module.id_formation == formation_id).all()
    modules_status = []

    for module in modules:
        module_link = db.query(UserModuleLink).filter(UserModuleLink.user_id == current_user.id_utilisateur, UserModuleLink.module_id == module.id_module).first()
        modules_status.append({
            "module": ModuleRead(
                id_module=module.id_module,
                titre=module.titre,
                description=module.description,
                url_image_module=module.url_image_module,
                formation=FormationRead(
                    id_formation=module.formation.id_formation,
                    titre=module.formation.titre,
                    description=module.formation.description,
                    url_image_formation=module.formation.url_image_formation,
                    instructeur=UtilisateurRead(
                        id_utilisateur=module.formation.instructeur.id_utilisateur,
                        nom=module.formation.instructeur.nom,
                        prenom=module.formation.instructeur.prenom,
                        email=module.formation.instructeur.email,
                        role=module.formation.instructeur.role,
                        est_actif=module.formation.instructeur.est_actif
                    )
                )
            ),
            "validated": bool(module_link)
        })

    return modules_status

