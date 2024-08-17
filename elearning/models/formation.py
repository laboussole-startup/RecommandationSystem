from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Formation(Base):
    __tablename__ = "formations"
    
    IDFormation = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Titre = Column(String(255), nullable=False)
    Description = Column(Text, nullable=False)
    IDInstructeur = Column(Integer, ForeignKey("utilisateurs.IDUtilisateur"))

    instructeur = relationship("Utilisateur", back_populates="formations")
    modules = relationship("Module", back_populates="formation")
    historiques = relationship("Historique", back_populates="formation")
