# app/main.py
from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import users  # después incluiremos más routers

# Crear las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir routers

@app.get("/")
def read_root():
    return {"message": "¡Tu API está viva! 🎉"}
