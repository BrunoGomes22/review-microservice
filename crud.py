from sqlalchemy.orm import Session
from sqlalchemy import func

import models, schemas

def create_review(db: Session, review_data: schemas.ReviewCreate):
    review = models.Review(**review_data.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_reviews_by_entity(db: Session, entity_id: str):
    return db.query(models.Review).filter(models.Review.entity_id == entity_id).all()

def delete_review(db: Session, review_id: int):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review:
        db.delete(review)
        db.commit()
    return review

def update_review(db: Session, review_id: int, review_data: schemas.ReviewUpdate):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review:
        for key, value in review_data.model_dump().items():
            setattr(review, key, value)
        db.commit()
        db.refresh(review)
    return review

def create_entity(db: Session, entity_data: schemas.EntityCreate):
    entity = models.Entity(**entity_data.model_dump())
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity

def get_review_by_id_and_entity(db: Session, review_id: int, entity_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id, models.Review.entity_id == entity_id).first()

def delete_review(db: Session, review_id: int):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review:
        db.delete(review)
        db.commit()
    return review

def get_entity_by_id(db: Session, entity_id: int):
    return db.query(models.Entity).filter(models.Entity.id == entity_id).first()

def delete_entity_and_reviews(db: Session, entity_id: int):
    # delete all reviews associated with the entity
    db.query(models.Review).filter(models.Review.entity_id == entity_id).delete()
    # delete the entity
    db.query(models.Entity).filter(models.Entity.id == entity_id).delete()
    db.commit()

def get_average_rating(db: Session, entity_id: int):
    average_rating = db.query(func.avg(models.Review.rating)).filter(models.Review.entity_id == entity_id).scalar()
    return average_rating or 0  # Return 0 if no reviews exist

def get_all_entities(db: Session):
    return db.query(models.Entity).all()
