from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Réponse(Base):
    __tablename__ = "réponses"
    
    IDRéponse = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Texte = Column(Text, nullable=False)
    EstCorrecte = Column(Boolean, nullable=False)
    IDQuestion = Column(Integer, ForeignKey("questions.IDQuestion"))

    question = relationship("Question", back_populates="reponses")
