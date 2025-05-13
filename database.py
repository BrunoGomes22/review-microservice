from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fastapi_user:securepassword@localhost/review_db")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fastapi_user:securepassword@database/review_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
