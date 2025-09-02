from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class FraudReport(Base):
    __tablename__ = "fraud_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    transfer_id = Column(Integer, ForeignKey("transfers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fraud_score = Column(Float, nullable=False)
    risk_factors = Column(JSON)  # Store identified risk factors
    ml_model_version = Column(String)
    is_confirmed_fraud = Column(Boolean, default=False)
    analyst_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    transfer = relationship("Transfer", back_populates="fraud_reports")
    user = relationship("User", back_populates="fraud_reports")


class FraudPattern(Base):
    __tablename__ = "fraud_patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    pattern_name = Column(String, nullable=False)
    pattern_type = Column(String, nullable=False)  # velocity, amount, geographic, etc.
    description = Column(Text)
    parameters = Column(JSON)  # Pattern-specific parameters
    threshold_score = Column(Float, default=0.5)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UserBehavior(Base):
    __tablename__ = "user_behaviors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String)
    ip_address = Column(String)
    user_agent = Column(String)
    device_fingerprint = Column(String)
    location_data = Column(JSON)
    behavior_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())