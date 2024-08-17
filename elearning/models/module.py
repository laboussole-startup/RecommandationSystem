# from sqlalchemy import Column, Integer, String, Text, ForeignKey
# from sqlalchemy.orm import relationship
# from core.database import Base

# class Module(Base):
#     __tablename__ = "modules"
    
#     IDModule = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     Titre = Column(String(255), nullable=False)
#     Description = Column(Text)
#     UrlImageModule = Column(String(255),nullable=False)
#     IDFormation = Column(Integer, ForeignKey("formations.IDFormation"))

#     formation = relationship("Formation", back_populates="modules")
#     cours = relationship("Cours", back_populates="module")
#     resumes = relationship("Résumé", back_populates="module")
#     quiz = relationship("Quiz", back_populates="module")
#     conferences = relationship("ConférenceVidéo", back_populates="module")

