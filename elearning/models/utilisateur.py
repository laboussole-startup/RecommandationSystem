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


# id = models.AutoField(primary_key=True)
# username = models.CharField(max_length=255, blank=True, null=True)
# first_name = models.CharField(max_length=255, blank=True, null=True)
# last_name = models.CharField(max_length=255, blank=True, null=True)
# niveau = models.CharField(max_length=50, blank=True, null=True)
# genre = models.CharField(max_length=10, blank=True, null=True)
# date_de_naissance = models.DateField(blank=True, null=True)
# email = models.CharField(unique=True, max_length=255, blank=True, null=True)
# centres_interet = models.CharField(max_length=255)
# telephone = models.CharField(max_length=20, blank=True, null=True)
# photo_de_profil = models.ImageField(upload_to='profiles/', blank=True, null=True)
# dernier_diplome = models.CharField(max_length=255, blank=True, null=True)
# serie = models.CharField(max_length=50, blank=True, null=True)
# is_staff = models.BooleanField(blank=True, null=True)
# is_superuser = models.BooleanField(blank=True, null=True)
# is_active = models.BooleanField(blank=True, null=False)
# last_login = models.DateTimeField(auto_now=True, null=True)
# date_joined = models.DateTimeField(auto_now_add=True, null=True)
# date_inscription = models.DateTimeField(auto_now_add=True, null=True)
# account_verification=models.TextField(blank=True,null=True)
# is_expert = models.BooleanField(blank=True, null=True)
# expert_id = models.IntegerField(blank=True, null=True)
