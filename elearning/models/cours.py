# from sqlalchemy import Column, Integer, String, ForeignKey, Text
# from sqlalchemy.orm import relationship
# from core.database import Base

# class Cours(Base):
#     __tablename__ = "cours"
    
#     IDCours = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     Titre = Column(String(255), nullable=False)
#     UrlVideosCours = Column(String(255), nullable=False)
#     UrlImageCours = Column(String(255),nullable=False)
#     Description = Column(Text, nullable=False)
#     IDModule = Column(Integer, ForeignKey("modules.IDModule"))

#     module = relationship("Module", back_populates="cours")



