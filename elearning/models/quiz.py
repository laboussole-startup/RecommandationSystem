from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Quiz(Base):
    __tablename__ = "quiz"
    
    IDQuiz = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Titre = Column(String(255), nullable=False)
    IDModule = Column(Integer, ForeignKey("modules.IDModule"))

    module = relationship("Module", back_populates="quiz")
    questions = relationship("Question", back_populates="quiz")
