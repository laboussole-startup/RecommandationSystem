import enum
from pydantic import BaseModel, EmailStr
from typing import Dict, List, Optional, Union
from datetime import date, datetime
from enum import Enum

class QuestionTypeEnum(enum.Enum):
    true_false = "true_false"
    single_choice = "single_choice"
    multiple_choice = "multiple_choice"

class RoleEnum(str, Enum):
    utilisateur = "utilisateur"
    instructeur = "instructeur"
    
# Schéma pour les utilisateurs
class UtilisateurBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    role: RoleEnum  # 'Utilisateur' ou 'Instructeur'
    est_actif: bool = True

class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str

class UtilisateurRead(UtilisateurBase):
    id_utilisateur: int

    class Config:
        orm_mode = True

# Schéma pour les formations
class FormationBase(BaseModel):
    titre: str
    description: Optional[str]
    url_image_formation: Optional[str]

class FormationCreate(FormationBase):
    id_instructeur: int

class FormationRead(FormationBase):
    id_formation: int
    instructeur: UtilisateurRead

    class Config:
        orm_mode = True

# Schéma pour les modules
class ModuleBase(BaseModel):
    titre: str
    description: Optional[str]
    url_image_module: Optional[str]

class ModuleCreate(ModuleBase):
    id_formation: int

class ModuleRead(ModuleBase):
    id_module: int
    formation: FormationRead

    class Config:
        orm_mode = True

# Schéma pour les leçons vidéos
class LeconVideoBase(BaseModel):
    titre: str
    description: Optional[str]
    url_video: str
    url_image_lecon: str

class LeconVideoCreate(LeconVideoBase):
    id_module: int

class LeconVideoRead(LeconVideoBase):
    id_lecon_video: int
    module: ModuleRead

    class Config:
        orm_mode = True

# Schéma pour les conférences vidéos
class ConferenceVideoBase(BaseModel):
    date_heure: datetime
    lien: str

class ConferenceVideoCreate(ConferenceVideoBase):
    id_module: int

class ConferenceVideoRead(ConferenceVideoBase):
    id_conference_video: int
    module: ModuleRead

    class Config:
        orm_mode = True

# Schéma pour les inscriptions aux formations
class UserFormationLinkBase(BaseModel):
    user_id: int
    formation_id: int

class UserFormationLinkCreate(UserFormationLinkBase):
    pass

class UserFormationLinkRead(UserFormationLinkBase):
    utilisateur: UtilisateurRead
    formation: FormationRead

    class Config:
        orm_mode = True

# Schéma pour les historiques
class HistoriqueBase(BaseModel):
    date_debut: Optional[date]
    date_fin: Optional[date]

class HistoriqueCreate(HistoriqueBase):
    id_utilisateur: int
    id_formation: int

class HistoriqueRead(HistoriqueBase):
    id_historique: int
    utilisateur: UtilisateurRead
    formation: FormationRead

    class Config:
        orm_mode = True


# Schéma pour la création d'un choix
class ChoiceCreate(BaseModel):
    texte: str
    est_correct: bool
    id_question: int

    class Config:
        orm_mode = True

# Schéma pour la sortie d'un choix
class ChoiceOut(BaseModel):
    id_choice: int
    texte: str
    est_correct: bool
    id_question: int

    class Config:
        orm_mode = True

# Schéma pour la création d'une question
class QuestionCreate(BaseModel):
    texte: str
    type_question: str
    id_quiz: int

    class Config:
        orm_mode = True

# Schéma pour la sortie d'une question
class QuestionOut(BaseModel):
    id_question: int
    texte: str
    type_question: str
    id_quiz: int

    class Config:
        orm_mode = True

# Schéma pour la création d'une réponse
class ReponseCreate(BaseModel):
    texte: str
    est_correcte: bool
    id_question: int

    class Config:
        orm_mode = True

# Schéma pour la sortie d'une réponse
class ReponseOut(BaseModel):
    id_reponse: int
    texte: str
    est_correcte: bool
    id_question: int

    class Config:
        orm_mode = True

# Schéma pour la création d'un quiz
class QuizCreate(BaseModel):
    titre: str
    description: Optional[str] = None
    id_module: int
    formation_id:int


    class Config:
        orm_mode = True

# Schéma pour la sortie d'un quiz
class QuizOut(BaseModel):
    id_quiz: int
    titre: str
    description: Optional[str] = None
    id_module: int

    class Config:
        orm_mode = True

# Schéma pour l'évaluation d'un quiz
class QuizEvaluation(BaseModel):
    true_false_answers: Optional[Dict[int, bool]] = None
    single_choice_answers: Optional[Dict[int, int]] = None
    multiple_choice_answers: Optional[Dict[int, List[int]]] = None

# Schéma pour le résultat de l'évaluation d'un quiz
class QuizEvaluationResult(BaseModel):
    score: float
    passed: bool
    total_questions: int
    correct_answers: int

# Schéma pour la correction d'une question
# class QuestionCorrection(BaseModel):
#     question_id: int
#     question_text: str
#     user_answer: Optional[Union[bool, int, List[int]]] = None
#     correct_answer: Optional[Union[bool, int, List[int]]] = None
#     is_correct: bool

# Schéma pour le résultat de la correction d'un quiz
# class QuizCorrectionResult(BaseModel):
#     score: float
#     passed: bool
#     total_questions: int
#     correct_answers: int
#     corrections: List[QuestionCorrection]

# Schéma pour l'inscription à une formation
class UserFormationLinkOut(BaseModel):
    id: int
    user_id: int
    formation_id: int

    class Config:
        orm_mode = True



# Schéma pour les informations de quiz
class QuizSummaryOut(BaseModel):
    id_quiz: int
    titre: str
    score: float
    passed: bool

    class Config:
        orm_mode = True

# Schéma pour les modules validés avec leurs notes
class ValidatedModuleOut(BaseModel):
    module: ModuleRead
    score: float

    class Config:
        orm_mode = True

# Schéma pour les quiz validés avec leurs notes
class ValidatedQuizOut(BaseModel):
    quiz: QuizSummaryOut
    score: float

    class Config:
        orm_mode = True

# Schéma pour les formations en cours ou terminées
class FormationStatusOut(BaseModel):
    formation: FormationRead
    in_progress: bool

    class Config:
        orm_mode = True



class QuestionCorrection(BaseModel):
    question_id: int
    question_text: str
    user_answer: Optional[str]
    correct_answer: Optional[str]
    is_correct: bool




class QuizCorrectionResult(BaseModel):
    score: float
    passed: bool
    total_questions: int
    correct_answers: int
    corrections: List[QuestionCorrection]

class QuizEvaluationResult(BaseModel):
    quiz_id: int
    total_questions: int
    correct_answers: int
    score: float
    passed: bool
    message: str
    corrections: List[QuestionCorrection]

class QuizAnswers(BaseModel):
    true_false_answers: Optional[Dict[int, bool]]
    single_choice_answers: Optional[Dict[int, int]]
    multiple_choice_answers: Optional[Dict[int, List[int]]]













class ChoiceOut(BaseModel):
    id_choice: int
    texte: str
    est_correct: bool

    class Config:
        from_attributes = True

class QuestionOut(BaseModel):
    id_question: int
    texte: str
    type_question: str
    choices: List[ChoiceOut]

    class Config:
        from_attributes = True

class QuizDetailsOut(BaseModel):
    id_quiz: int
    titre: str
    description: str
    questions: List[QuestionOut]

    class Config:
        from_attributes = True

class UserAnswer(BaseModel):
    id_question: int
    id_choice: int

class QuestionResult(BaseModel):
    id_question: int
    correct: bool
    correct_choice: Optional[int]
    user_choice: int

class QuizSubmission(BaseModel):
    quiz_id: int
    answers: List[UserAnswer]

class QuizResult(BaseModel):
    quiz_id: int
    total_questions: int
    correct_answers: int
    score: float
    passed: bool
    results: List[QuestionResult]



class EventCreate(BaseModel):
    summary: str
    description: str
    start_time: datetime
    end_time: datetime
    attendees: List[str]

class EventRead(BaseModel):
    id: int
    module_id: int
    event_id: str
    summary: str
    description: str
    start_time: datetime
    end_time: datetime
    hangout_link: str

    class Config:
        orm_mode = True
