from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    bio = Column(Text, nullable=False)
    interests = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    interactions = relationship("Interaction", back_populates="profile")


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)
    event_description = Column(Text, nullable=False)
    interests = Column(String(500), nullable=True)
    themes = Column(Text, nullable=True)          # JSON-encoded list of extracted themes
    starters = Column(Text, nullable=False)        # JSON-encoded list of generated starters
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="interactions")
    feedback = relationship("Feedback", back_populates="interaction", uselist=False)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"), nullable=False)
    useful = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    interaction = relationship("Interaction", back_populates="feedback")


class FactCheckLog(Base):
    __tablename__ = "fact_check_logs"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    source_url = Column(String(500), nullable=True)
    found = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
