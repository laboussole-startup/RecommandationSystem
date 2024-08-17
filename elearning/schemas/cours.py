# from pydantic import BaseModel
# from typing import Optional

# class CoursBase(BaseModel):
#     Titre: str
#     Description: str
#     UrlImageCours: str
#     UrlVideosCours: str

# class CoursCreate(CoursBase):
#     IDModule: int

# class CoursInDB(CoursBase):
#     IDCours: int
#     IDModule: int

#     class Config:
#         orm_mode = True
