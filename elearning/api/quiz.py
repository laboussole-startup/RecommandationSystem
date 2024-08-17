from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_current_user  # Cette fonction doit être définie pour obtenir l'utilisateur actuel
from elearning.models.modelsSQLAlchemy import Choice, Question, Quiz, Reponse, UserFormationLink, Utilisateur
from elearning.schemas.SchemasPydantic import (
    ChoiceCreate, ChoiceOut, QuestionCreate, QuestionOut, QuestionResult, QuizAnswers, QuizCreate, QuizDetailsOut, 
    QuizEvaluation, QuizCorrectionResult, QuizEvaluationResult, QuizOut, QuizResult, QuizSubmission, ReponseCreate, ReponseOut, UserFormationLinkOut, QuestionCorrection
)


router = APIRouter()

# Endpoint pour créer un nouveau quiz
@router.post("/quiz/", response_model=QuizOut)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)):
    """
    Endpoint pour créer un nouveau quiz. 
    Accessible uniquement par un instructeur.
    """
    print(current_user.role.value)
    if current_user.role.value != 'instructeur':
        raise HTTPException(status_code=403, detail="Accès interdit")
    
    db_quiz = Quiz(**quiz.dict())
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

# Endpoint pour créer une nouvelle question pour un quiz
@router.post("/questions/", response_model=QuestionOut)
def create_question(question: QuestionCreate, db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)):
    """
    Endpoint pour créer une nouvelle question pour un quiz.
    Accessible uniquement par un instructeur.
    """
    print(current_user.role)

    if current_user.role.value != 'instructeur':
        raise HTTPException(status_code=403, detail="Accès interdit")

    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

# Endpoint pour créer une nouvelle réponse pour une question de type true_false
@router.post("/reponses/", response_model=ReponseOut)
def create_reponse(reponse: ReponseCreate, db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)):
    """
    Endpoint pour créer une nouvelle réponse pour une question de type true_false.
    Accessible uniquement par un instructeur.
    """
    if current_user.role.value != 'instructeur':
        raise HTTPException(status_code=403, detail="Accès interdit")
    
    db_reponse = Reponse(**reponse.dict())
    db.add(db_reponse)
    db.commit()
    db.refresh(db_reponse)
    return db_reponse

# Endpoint pour créer un nouveau choix pour une question de type single_choice ou multiple_choice
@router.post("/choices/", response_model=ChoiceOut)
def create_choice(choice: ChoiceCreate, db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)):
    """
    Endpoint pour créer un nouveau choix pour une question de type single_choice ou multiple_choice.
    Accessible uniquement par un instructeur.
    """
    if current_user.role.value != 'instructeur':
        raise HTTPException(status_code=403, detail="Accès interdit")
    
    db_choice = Choice(**choice.dict())
    db.add(db_choice)
    db.commit()
    db.refresh(db_choice)
    return db_choice

# Endpoint pour récupérer tous les quiz
@router.get("/quiz/", response_model=List[QuizOut])
def get_quizs(db: Session = Depends(get_db)):
    """
    Endpoint pour récupérer tous les quiz.
    Accessible à tous les utilisateurs connectés.
    """
    return db.query(Quiz).all()

# Endpoint pour récupérer toutes les questions d'un quiz donné
@router.get("/quiz/{quiz_id}/questions/", response_model=List[QuestionOut])
def get_questions(quiz_id: int, db: Session = Depends(get_db)):
    """
    Endpoint pour récupérer toutes les questions d'un quiz donné.
    Accessible à tous les utilisateurs connectés.
    """
    return db.query(Question).filter(Question.id_quiz == quiz_id).all()





@router.get("/quiz/{quiz_id}/questions", response_model=QuizDetailsOut)
def get_quiz_details(quiz_id: int, db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)):
    """
    Endpoint pour récupérer les détails d'un quiz, y compris les questions et les choix associés.
    """
    quiz = db.query(Quiz).filter(Quiz.id_quiz == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz introuvable")
    
    questions = db.query(Question).filter(Question.id_quiz == quiz_id).all()
    quiz_questions = []

    for question in questions:
        choices = db.query(Choice).filter(Choice.id_question == question.id_question).all()
        quiz_questions.append(
            QuestionOut(
                id_question=question.id_question,
                texte=question.texte,
                type_question=question.type_question,
                choices=[ChoiceOut.from_orm(choice) for choice in choices]
            )
        )

    return QuizDetailsOut(
        id_quiz=quiz.id_quiz,
        titre=quiz.titre,
        description=quiz.description,
        questions=quiz_questions
    )








@router.post("/quiz/{quiz_id}/submit", response_model=QuizResult)
def submit_quiz(quiz_submission: QuizSubmission, db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)):
    """
    Endpoint pour soumettre les réponses d'un quiz et obtenir le résultat.
    """
    quiz = db.query(Quiz).filter(Quiz.id_quiz == quiz_submission.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz introuvable")

    # Récupérer toutes les questions du quiz
    questions = db.query(Question).filter(Question.id_quiz == quiz.id_quiz).all()
    total_questions = len(questions)
    correct_answers = 0
    results = []

    # Parcourir les réponses de l'utilisateur et évaluer chaque question
    for user_answer in quiz_submission.answers:
        question = db.query(Question).filter(Question.id_question == user_answer.id_question).first()
        if not question:
            raise HTTPException(status_code=400, detail=f"Question ID {user_answer.id_question} introuvable")
        
        correct_choice = db.query(Choice).filter(Choice.id_question == question.id_question, Choice.est_correct == True).first()
        user_choice = db.query(Choice).filter(Choice.id_choice == user_answer.id_choice).first()

        if user_choice and user_choice.est_correct:
            correct_answers += 1
            correct = True
        else:
            correct = False

        results.append(QuestionResult(
            id_question=question.id_question,
            correct=correct,
            correct_choice=correct_choice.id_choice if correct_choice else None,
            user_choice=user_answer.id_choice
        ))

    score = (correct_answers / total_questions) * 100
    passed = score >= 60  # Supposons que 60% est le seuil de réussite

    return QuizResult(
        quiz_id=quiz.id_quiz,
        total_questions=total_questions,
        correct_answers=correct_answers,
        score=score,
        passed=passed,
        results=results
    )
