from sqlalchemy.orm import Session

import models, schemas


def get_image_id(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def create_image(db: Session, image: schemas.ImageCreate):
    db_image = models.Image(image=image.bytes_img)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def get_images(db: Session, page: int = 1, limit: int = 10):
    skip = (1-page)*limit
    rez = db.query(models.Image).offset(skip).limit(limit).all()
    return rez
