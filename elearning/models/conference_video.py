# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from core.database import Base

# class ConférenceVidéo(Base):
#     __tablename__ = "conférences_vidéo"
    
#     IDConférenceVidéo = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     DateHeure = Column(DateTime, nullable=False)
#     Lien = Column(String(255), nullable=False)
#     IDModule = Column(Integer, ForeignKey("modules.IDModule"))

#     module = relationship("Module", back_populates="conferences")
