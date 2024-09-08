import enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Enum, Date, DateTime,Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Enum for user roles
class RoleEnum(enum.Enum):
    utilisateur = "utilisateur"
    instructeur = "instructeur"

# User model
class Utilisateurtest(Base):
    __tablename__ = 'utilisateurs'
    
    id_utilisateur = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), nullable=False)
    prenom = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    mot_de_passe = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    est_actif = Column(Boolean, default=True)
    
    formations = relationship('Formation', back_populates='instructeur')
    historiques = relationship('Historique', back_populates='utilisateur')
    inscrits = relationship('UserFormationLink', back_populates='utilisateur')

# Formation model
class Formation(Base):
    __tablename__ = 'formations'
    
    id_formation = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String(255), nullable=False)
    description = Column(Text)
    id_instructeur = Column(Integer, ForeignKey('utilisateurs.id_utilisateur'))
    url_image_formation = Column(String(255))
    
    instructeur = relationship('Utilisateurtest', back_populates='formations')
    modules = relationship('Module', back_populates='formation')
    historiques = relationship('Historique', back_populates='formation')
    inscrits = relationship('UserFormationLink', back_populates='formation')
    quiz = relationship('Quiz', back_populates='formation')

# Module model
class Module(Base):
    __tablename__ = 'modules'
    
    id_module = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String(255), nullable=False)
    description = Column(Text)
    id_formation = Column(Integer, ForeignKey('formations.id_formation'))
    url_image_module = Column(String(255))
    events = relationship("Event", back_populates="module")
    formation = relationship('Formation', back_populates='modules')
    lecons_videos = relationship('LeconVideo', back_populates='module')
    quizs = relationship('Quiz', back_populates='module')
    conferences_videos = relationship('ConferenceVideo', back_populates='module')

# Leçon vidéo model
class LeconVideo(Base):
    __tablename__ = 'lecons_videos'
    
    id_lecon_video = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String(255), nullable=False)
    description = Column(Text)
    url_video = Column(String(255), nullable=False)
    url_image_lecon = Column(String(255), nullable=False)
    id_module = Column(Integer, ForeignKey('modules.id_module'))
    
    module = relationship('Module', back_populates='lecons_videos')

# Quiz model
class Quiz(Base):
    __tablename__ = 'quiz'
    
    id_quiz = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String(255), nullable=False)
    description = Column(Text)
    id_module = Column(Integer, ForeignKey('modules.id_module'))
    formation_id = Column(Integer, ForeignKey('formations.id_formation'))
    
    
    module = relationship('Module', back_populates='quizs')
    formation = relationship('Formation', back_populates='quiz')
    questions = relationship('Question', back_populates='quiz')

# Question model
class Question(Base):
    __tablename__ = 'questions'
    
    id_question = Column(Integer, primary_key=True, autoincrement=True)
    texte = Column(Text, nullable=False)
    type_question = Column(Enum('true_false', 'single_choice', 'multiple_choice', name='question_type'), nullable=False)
    id_quiz = Column(Integer, ForeignKey('quiz.id_quiz'))
    
    quiz = relationship('Quiz', back_populates='questions')
    reponses = relationship('Reponse', back_populates='question')
    choices = relationship('Choice', back_populates='question')

# Réponse model (for true_false questions)
class Reponse(Base):
    __tablename__ = 'reponses'
    
    id_reponse = Column(Integer, primary_key=True, autoincrement=True)
    texte = Column(Text, nullable=False)
    est_correcte = Column(Boolean, nullable=False)
    id_question = Column(Integer, ForeignKey('questions.id_question'))
    
    question = relationship('Question', back_populates='reponses')

# Choice model (for single_choice and multiple_choice questions)
class Choice(Base):
    __tablename__ = 'choices'
    
    id_choice = Column(Integer, primary_key=True, autoincrement=True)
    texte = Column(Text, nullable=False)
    est_correct = Column(Boolean, default=False)
    id_question = Column(Integer, ForeignKey('questions.id_question'))
    
    question = relationship('Question', back_populates='choices')

# UserFormationLink model for user-formation relationship
class UserFormationLink(Base):
    __tablename__ = 'user_formation_link'
    
    user_id = Column(Integer, ForeignKey('utilisateurs.id_utilisateur'), primary_key=True)
    formation_id = Column(Integer, ForeignKey('formations.id_formation'), primary_key=True)
    
    utilisateur = relationship('Utilisateurtest', back_populates='inscrits')
    formation = relationship('Formation', back_populates='inscrits')




# Historique model
class Historique(Base):
    __tablename__ = 'historiques'
    
    id_historique = Column(Integer, primary_key=True, autoincrement=True)
    id_utilisateur = Column(Integer, ForeignKey('utilisateurs.id_utilisateur'))
    id_formation = Column(Integer, ForeignKey('formations.id_formation'))
    date_debut = Column(Date)
    date_fin = Column(Date)
    
    utilisateur = relationship('Utilisateurtest', back_populates='historiques')
    formation = relationship('Formation', back_populates='historiques')

# ConferenceVideo model
class ConferenceVideo(Base):
    __tablename__ = 'conferences_videos'
    
    id_conference_video = Column(Integer, primary_key=True, autoincrement=True)
    date_heure = Column(DateTime, nullable=False)
    lien = Column(String(255), nullable=False)
    id_module = Column(Integer, ForeignKey('modules.id_module'))
    
    module = relationship('Module', back_populates='conferences_videos')





# class UserFormationLink(Base):
#     __tablename__ = 'user_formation_link'
    
#     user_id = Column(Integer, ForeignKey('utilisateurs.id_utilisateur'), primary_key=True)
#     formation_id = Column(Integer, ForeignKey('formations.id_formation'), primary_key=True)
    
#     utilisateur = relationship('Utilisateur', back_populates='inscrits')
#     formation = relationship('Formation', back_populates='inscrits')

class UserModuleLink(Base):
    __tablename__ = 'user_module_link'
    
    user_id = Column(Integer, ForeignKey('utilisateurs.id_utilisateur'), primary_key=True)
    module_id = Column(Integer, ForeignKey('modules.id_module'), primary_key=True)
    score = Column(Float)

class UserQuizLink(Base):
    __tablename__ = 'user_quiz_link'
    
    user_id = Column(Integer, ForeignKey('utilisateurs.id_utilisateur'), primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quiz.id_quiz'), primary_key=True)
    score = Column(Float)
    passed = Column(Boolean)


class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String(255), unique=True, nullable=False)  # Spécifiez la longueur ici
    module_id = Column(Integer, ForeignKey('modules.id_module'))
    summary = Column(String(255), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    hangout_link = Column(String(255))
    
    module = relationship('Module', back_populates='events')