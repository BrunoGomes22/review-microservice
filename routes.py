from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas, crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/v1/entities", response_model=schemas.EntityResponse)
def create_entity(entity: schemas.EntityCreate, db: Session = Depends(get_db)):
    return crud.create_entity(db, entity)

@router.post("/v1/reviews", response_model=schemas.ReviewResponse)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db, review)

@router.get("/v1/entities/{entity_id}/reviews", response_model=list[schemas.ReviewResponse])
def get_reviews(entity_id: int, db: Session = Depends(get_db)):
    return crud.get_reviews_by_entity(db, entity_id)

@router.delete("/v1/entities/{entity_id}/reviews/{review_id}")
def delete_review(entity_id: int, review_id: int, db: Session = Depends(get_db)):
    review = crud.get_review_by_id_and_entity(db, review_id, entity_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    crud.delete_review(db, review_id)
    return {"message": "Review deleted successfully"}

@router.put("/v1/entities/{entity_id}/reviews/{review_id}", response_model=schemas.ReviewResponse)
def update_review(entity_id: int, review_id: int, review: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    existing_review = crud.get_review_by_id_and_entity(db, review_id, entity_id)
    if not existing_review:
        raise HTTPException(status_code=404, detail="Review not found")
    updated_review = crud.update_review(db, review_id, review)
    return updated_review

@router.delete("/v1/entities/{entity_id}", response_model=dict)
def delete_entity(entity_id: int, db: Session = Depends(get_db)):
    entity = crud.get_entity_by_id(db, entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    crud.delete_entity_and_reviews(db, entity_id)
    return {"message": "Entity and associated reviews deleted successfully"}