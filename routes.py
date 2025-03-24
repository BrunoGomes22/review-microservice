from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas, crud
from uuid import UUID

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/v1/reviews", response_model=schemas.ReviewResponse)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db, review)

@router.get("/v1/entities/{entity_id}/reviews", response_model=list[schemas.ReviewResponse])
def get_reviews(entity_id: UUID, db: Session = Depends(get_db)):
    return crud.get_reviews_by_entity(db, entity_id)

@router.delete("/v1/reviews/{review_id}")
def delete_review(review_id: UUID, db: Session = Depends(get_db)):
    review = crud.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    crud.delete_review(db, review_id)
    return {"message": "Review deleted successfully"}

@router.put("/v1/reviews/{review_id}", response_model=schemas.ReviewResponse)
def update_review(review_id: UUID, review: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    existing_review = crud.get_review(db, review_id)
    if not existing_review:
        raise HTTPException(status_code=404, detail="Review not found")
    updated_review = crud.update_review(db, review_id, review)
    return updated_review