from sqlalchemy.orm import Session
from elearning.models.modelsSQLAlchemy import Module
from elearning.schemas.SchemasPydantic import ModuleCreate




def createModule(db: Session, module: ModuleCreate):
    # Example implementation
    db_Module = Module(
        titre =module.titre,
        description=module.description,
        url_image_module= module.url_image_module,
        id_formation=module.id_formation
    )
    db.add(db_Module)
    db.commit()
    db.refresh(db_Module)
    return db_Module


def get_module(db: Session, module_id: int):
    return db.query(Module).filter(Module.id_module == module_id).first()

def get_modules(db: Session, formation_id):
    return db.query(Module).filter(Module.id_formation==formation_id).all()


