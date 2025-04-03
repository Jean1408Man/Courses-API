# app/test_db_connection.py
from app.db.database import SessionLocal
from sqlalchemy import text

def test_connection():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1"))
        print("✅ Conexión exitosa:", result.scalar())  # Debería imprimir: 1
    except Exception as e:
        print("❌ Error en la conexión:", e)
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
