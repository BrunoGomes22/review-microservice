from sqlalchemy import Column, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    rating = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
    timestamp = Column(DateTime, default=func.now())
"""
class Product(Base): # this table is used for testing purposes, when deploying the microservice, this table should be removed
    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_type = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    product_price = Column(Float, nullable=False)
    product_seller = Column(String, nullable=True)
    reviews = Column(UUID(as_uuid=True), nullable=True)  # Optional: Array of UUIDs if needed
"""