from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, DECIMAL, func

from core.database import Base
from sqlalchemy.orm import relationship



from core.database import Base



# class CentreInteret(Base):
#     __tablename__ = "centre_interet"
#     id = Column(Integer, primary_key=True, index=True)
#     nom = Column(String(255))
#     filieres_id = Column(Integer, ForeignKey('filieres.filieres_id'))
#     filiere = relationship("Filiere", back_populates="centre_interet")

# class Universite(Base):
#     __tablename__ = 'universite'

#     universite_id = Column(Integer, primary_key=True, autoincrement=True)
#     nom = Column(String(255), unique=True, nullable=False)
#     ville = Column(String(255), nullable=False)
#     descriptif = Column(Text, nullable=False)
#     email = Column(String(255), nullable=False)
#     telephone = Column(String(255), nullable=False)
#     site_web = Column(String(255))
#     facultes = relationship("Faculte", back_populates="universite")
# class Faculte(Base):
#     __tablename__ = 'faculte'

#     faculte_id = Column(Integer, primary_key=True, autoincrement=True)
#     nom = Column(String(255), nullable=False)
#     descriptif = Column(Text)
#     condition_admission = Column(Text)
#     email = Column(String(255))
#     telephone = Column(String(255))
#     universite_id = Column(Integer, ForeignKey('universite.universite_id', ondelete='CASCADE'), nullable=False)
#     universite = relationship("Universite", back_populates="facultes")
#     universite_id = Column(Integer, ForeignKey('universite.universite_id'))
    

# class Filiere(Base):
#     __tablename__ = "filieres"
#     filieres_id = Column(Integer, primary_key=True, index=True)
#     nom = Column(String(255), nullable=False)
#     descriptif = Column(Text, nullable=False)
#     duree = Column(Integer, nullable=False)
#     cout = Column(DECIMAL(10, 2), nullable=False)
#     langue_enseignement = Column(String(50), nullable=False)
#     diplome_delivre = Column(String(255), nullable=False)
#     images_pc = Column(Text)
#     images_telephone = Column(Text)
#     images_tablettes = Column(Text)
#     faculte_id = Column(Integer, ForeignKey('facultes.faculte_id', ondelete='CASCADE'), nullable=False)
#     centre_interet = Column(Text)











class Universite(Base):
    __tablename__ = 'universite'

    universite_id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), unique=True, nullable=False)
    ville = Column(String(255), nullable=False)
    pays = Column(String(255), nullable=False)
    descriptif = Column(Text, nullable=False)
    email = Column(String(255), nullable=False)
    telephone = Column(String(255), nullable=False)
    logo = Column(Text)
    site_web = Column(String(255))
    facultes = relationship("Faculte", back_populates="universite")

class Faculte(Base):
    __tablename__ = 'faculte'

    faculte_id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), nullable=False)
    descriptif = Column(Text)
    condition_admission = Column(Text)
    email = Column(String(255))
    telephone = Column(String(255))
    images_pc = Column(Text)
    images_telephone = Column(Text)
    images_tablettes = Column(Text)
    universite_id = Column(Integer, ForeignKey('universite.universite_id', ondelete='CASCADE'), nullable=False)
    universite = relationship("Universite", back_populates="facultes")
    filieres = relationship("Filiere", back_populates="faculte")

class Filiere(Base):
    __tablename__ = "filieres"
    filieres_id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    descriptif = Column(Text, nullable=False)
    duree = Column(Integer, nullable=False)
    cout = Column(DECIMAL(10, 2), nullable=False)
    langue_enseignement = Column(String(50), nullable=False)
    diplome_delivre = Column(String(255), nullable=False)
    images_pc = Column(Text)
    images_telephone = Column(Text)
    images_tablettes = Column(Text)
    faculte_id = Column(Integer, ForeignKey('faculte.faculte_id', ondelete='CASCADE'), nullable=False)
    faculte = relationship("Faculte", back_populates="filieres")
    centre_interet = Column(Text)

class metiers(Base):
    __tablename__ = "metiers"
    
    id_metiers = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    entreprisesrecrutent = Column(Text, nullable=False)
    salairemoyen = Column(Text, nullable=False)
    competencescles = Column(Text, nullable=False)
    logo = Column(String(255), nullable=True)
    images_pc = Column(String(255), nullable=True)
    principales_missions = Column(Text, nullable=True)
    images_telephone = Column(String(255), nullable=True)
    images_tablettes = Column(String(255), nullable=True)
    faculte = Column(String(255), nullable=True)
    ecole = Column(String(255), nullable=True)
    filiere = Column(String(255), nullable=True)



# class User(Base):
#     __tablename__ = 'user'
#     user_id = Column(Integer, primary_key=True, autoincrement=True)
#     user_name = Column(String(255))

# class SearchHistory(Base):
#     __tablename__ = 'recherches'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('user.user_id'))
#     keywords = Column(String(255))
#     timestamp = Column(DateTime, default=datetime.utcnow)

#     # Relationship to User
#     user = relationship("User", backref="search_history")


class Utilisateur(Base):
    __tablename__ = 'utilisateur'
    
    id_utilisateur = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    pays = Column(String(255))
    ville = Column(String(255))
    niveau = Column(String(50))
    genre = Column(String(10))
    date_de_naissance = Column(DateTime)
    mail = Column(String(255))
    mot_de_passe = Column(String(255))
    telephone = Column(String(20))
    centre_interet = Column(Text)
    photo_de_profil = Column(Text)  # Bytea is not natively supported by all DBs, use Text
    dernier_diplome = Column(String(255))
    serie = Column(String(50))
    derniere_connexion = Column(DateTime)
    date_inscription = Column(DateTime)

    recherches = relationship('Recherches', back_populates='utilisateur')

class Recherches(Base):
    __tablename__ = 'recherches'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_utilisateur = Column(Integer, ForeignKey('utilisateur.id_utilisateur'))
    date_heure = Column(DateTime)
    mots_cles = Column(String(255))

    utilisateur = relationship('Utilisateur', back_populates='recherches')
