from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Question(Base):
    __tablename__ = "questions"
    
    IDQuestion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Texte = Column(Text, nullable=False)
    IDQuiz = Column(Integer, ForeignKey("quiz.IDQuiz"))

    quiz = relationship("Quiz", back_populates="questions")
    reponses = relationship("Réponse", back_populates="question")
