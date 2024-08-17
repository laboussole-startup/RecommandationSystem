from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from core.database import Base

class Historique(Base):
    __tablename__ = "historiques"
    
    IDHistorique = Column(Integer, primary_key=True, index=True, autoincrement=True)
    IDUtilisateur = Column(Integer, ForeignKey("utilisateurs.IDUtilisateur"))
    IDFormation = Column(Integer, ForeignKey("formations.IDFormation"))
    DateDébut = Column(Date)
    DateFin = Column(Date)

    utilisateur = relationship("Utilisateur", back_populates="historiques")
    formation = relationship("Formation", back_populates="historiques")
