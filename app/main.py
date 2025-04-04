# app/main.py
from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import users  # después incluiremos más routers
from app.routers import all_routers



app = FastAPI()

# Incluir routers
for router in all_routers:
    app.include_router(router)
# Crear las tablas
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
@app.get("/")
def read_root():
    return {"message": "¡Tu API está viva! 🎉"}
