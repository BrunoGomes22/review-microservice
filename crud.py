from sqlalchemy.orm import Session
from sqlalchemy import func

import models, schemas
from uuid import UUID

def create_review(db: Session, review_data: schemas.ReviewCreate):
    review = models.Review(**review_data.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_reviews_by_entity(db: Session, entity_id: UUID):
    return db.query(models.Review).filter(models.Review.entity_id == entity_id).all()

def delete_review(db: Session, review_id: UUID):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review:
        db.delete(review)
        db.commit()
    return review

def update_review(db: Session, review_id: UUID, review_data: schemas.ReviewUpdate):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review:
        for key, value in review_data.model_dump().items():
            if value is not None:  # Only update fields that were provided
                setattr(review, key, value)
        db.commit()
        db.refresh(review)
    return review

def delete_review(db: Session, review_id: int):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review:
        db.delete(review)
        db.commit()
    return review

def get_review(db: Session, review_id: UUID):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def get_average_rating(db: Session, entity_id: UUID):
    average_rating = db.query(func.avg(models.Review.rating)).filter(models.Review.entity_id == entity_id).scalar()
    return average_rating or 0  # Return 0 if no reviews exist
