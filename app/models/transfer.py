from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class TransferStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    FLAGGED = "flagged"


class TransferType(str, enum.Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"


class Transfer(Base):
    __tablename__ = "transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    reference_id = Column(String, unique=True, index=True, nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for withdrawals
    receiver_external_id = Column(String)  # For external transfers
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    description = Column(String)
    status = Column(Enum(TransferStatus), default=TransferStatus.PENDING)
    transfer_type = Column(Enum(TransferType), default=TransferType.INTERNAL)
    fraud_score = Column(Float, default=0.0)
    is_flagged = Column(Boolean, default=False)
    flagged_reason = Column(String)
    processed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_transfers")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_transfers")
    fraud_reports = relationship("FraudReport", back_populates="transfer")