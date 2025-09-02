from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.transfer import TransferStatus, TransferType


class TransferBase(BaseModel):
    amount: float = Field(..., gt=0, description="Transfer amount must be positive")
    currency: str = Field(default="USD", description="Currency code")
    description: Optional[str] = None


class TransferCreate(TransferBase):
    receiver_id: Optional[int] = None
    receiver_external_id: Optional[str] = None
    transfer_type: TransferType = TransferType.INTERNAL


class TransferResponse(TransferBase):
    id: int
    reference_id: str
    sender_id: int
    receiver_id: Optional[int]
    status: TransferStatus
    transfer_type: TransferType
    fraud_score: float
    is_flagged: bool
    created_at: datetime
    
    class Config:
        from_attributes = True