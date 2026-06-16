from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from core.logging_config import logger  
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    status = Column(String, default="open")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NexusMonitor API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise
    finally:
        db.close()

@app.get("/api/incidents")
def get_incidents(db: Session = Depends(get_db)):
    logger.info("Запрос списка инцидентов")
    try:
        incidents = db.query(Incident).all()
        incidents_data = [
            {"id": inc.id, "title": inc.title, "status": inc.status}
            for inc in incidents
        ]
        return {"status": "success", "data": incidents_data}
    except Exception as e:
        logger.error(f"Error fetching incidents: {str(e)}")
        return {"status": "error", "data": [], "message": str(e)}
