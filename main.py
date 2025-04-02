from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # Import StaticFiles
from database import engine, Base
from routes import router

app = FastAPI(title="Review Microservice")

# Create database tables
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")  # Mount the static directory

@app.get("/")
def root():
    return {"message": "Review Microservice is running!"}