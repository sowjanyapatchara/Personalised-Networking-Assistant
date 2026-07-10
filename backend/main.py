import json
import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database import Base, engine, get_db
import models
import schemas
from services.gemini_service import generate_themes_and_starters
from services.wikipedia_service import fact_check

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personalized Networking Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")


# ---------- API ROUTES ----------

@app.post("/api/v1/generate", response_model=schemas.GenerateResponse)
def generate_starters(payload: schemas.GenerateRequest, db: Session = Depends(get_db)):
    try:
        result = generate_themes_and_starters(
            bio=payload.bio,
            event_description=payload.event_description,
            interests=payload.interests or "",
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    profile = models.UserProfile(
        name=payload.name,
        bio=payload.bio,
        interests=payload.interests,
    )
    db.add(profile)
    db.flush()

    interaction = models.Interaction(
        profile_id=profile.id,
        event_description=payload.event_description,
        interests=payload.interests,
        themes=json.dumps(result["themes"]),
        starters=json.dumps(result["starters"]),
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return schemas.GenerateResponse(
        interaction_id=interaction.id,
        themes=result["themes"],
        starters=result["starters"],
        created_at=interaction.created_at,
    )


@app.get("/api/v1/verify", response_model=schemas.VerifyResponse)
def verify_fact(query: str, db: Session = Depends(get_db)):
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query parameter 'query' is required")

    result = fact_check(query)

    log = models.FactCheckLog(
        query=query,
        summary=result.get("summary"),
        source_url=result.get("source_url"),
        found=result.get("found", False),
    )
    db.add(log)
    db.commit()

    return schemas.VerifyResponse(
        query=query,
        found=result.get("found", False),
        summary=result.get("summary"),
        source_url=result.get("source_url"),
    )


@app.post("/api/v1/feedback")
def submit_feedback(payload: schemas.FeedbackRequest, db: Session = Depends(get_db)):
    interaction = db.query(models.Interaction).filter(models.Interaction.id == payload.interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    existing = db.query(models.Feedback).filter(models.Feedback.interaction_id == payload.interaction_id).first()
    if existing:
        existing.useful = payload.useful
    else:
        db.add(models.Feedback(interaction_id=payload.interaction_id, useful=payload.useful))

    db.commit()
    return {"status": "ok", "interaction_id": payload.interaction_id, "useful": payload.useful}


@app.get("/api/v1/history", response_model=list[schemas.HistoryItem])
def get_history(db: Session = Depends(get_db)):
    interactions = (
        db.query(models.Interaction)
        .order_by(desc(models.Interaction.created_at))
        .limit(50)
        .all()
    )

    items = []
    for i in interactions:
        fb = i.feedback.useful if i.feedback else None
        items.append(
            schemas.HistoryItem(
                id=i.id,
                event_description=i.event_description,
                interests=i.interests,
                themes=json.loads(i.themes) if i.themes else [],
                starters=json.loads(i.starters) if i.starters else [],
                created_at=i.created_at,
                feedback=fb,
            )
        )
    return items


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


# ---------- FRONTEND (static multi-page site) ----------

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/{page_name}.html")
def serve_page(page_name: str):
    file_path = os.path.join(FRONTEND_DIR, f"{page_name}.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Page not found")
