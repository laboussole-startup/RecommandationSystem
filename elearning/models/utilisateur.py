# from sqlalchemy import Boolean, Column, Integer, String, Enum
# from sqlalchemy.orm import relationship
# from core.database import Base

# class Utilisateur(Base):
#     __tablename__ = "utilisateurs"
    
#     IDUtilisateur = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     Nom = Column(String(255), nullable=False)
#     Prénom = Column(String(255), nullable=False)
#     Email = Column(String(255), unique=True, index=True, nullable=False)
#     MotDePasse = Column(String(255), nullable=False)
#     Role = Column(Enum('Utilisateur', 'Instructeur'), nullable=False)
#     is_active = Column(Boolean, default=True)
#     formations = relationship("Formation", back_populates="instructeur")
#     historiques = relationship("Historique", back_populates="utilisateur")
