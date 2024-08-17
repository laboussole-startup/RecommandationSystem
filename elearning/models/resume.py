
# from sqlalchemy import Column, Integer, Text, ForeignKey
# from sqlalchemy.orm import relationship
# from core.database import Base

# class Résumé(Base):
#     __tablename__ = "résumés"
    
#     IDRésumé = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     Texte = Column(Text, nullable=False)
#     Images = Column(Text)
#     IDModule = Column(Integer, ForeignKey("modules.IDModule"))

#     module = relationship("Module", back_populates="resumes")
