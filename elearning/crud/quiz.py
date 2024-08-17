from sqlalchemy.orm import Session
from elearning.models.modelsSQLAlchemy import Choice, Question, Quiz, Reponse
from elearning.schemas.SchemasPydantic import (
    ChoiceCreate, QuestionCreate, QuizCreate, ReponseCreate
)

# Fonction pour créer un quiz
def create_quiz(db: Session, quiz: QuizCreate):
    db_quiz = Quiz(**quiz.dict())
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

# Fonction pour créer une question
def create_question(db: Session, question: QuestionCreate):
    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

# Fonction pour créer une réponse (true_false)
def create_reponse(db: Session, reponse: ReponseCreate):
    db_reponse = Reponse(**reponse.dict())
    db.add(db_reponse)
    db.commit()
    db.refresh(db_reponse)
    return db_reponse

# Fonction pour créer un choix (single_choice et multiple_choice)
def create_choice(db: Session, choice: ChoiceCreate):
    db_choice = Choice(**choice.dict())
    db.add(db_choice)
    db.commit()
    db.refresh(db_choice)
    return db_choice

# Fonction pour obtenir tous les quiz
def get_quizs(db: Session):
    return db.query(Quiz).all()

# Fonction pour obtenir toutes les questions d'un quiz
def get_questions(db: Session, quiz_id: int):
    return db.query(Question).filter(Question.id_quiz == quiz_id).all()

