from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid

from app.core.database import get_db
from app.models.user import User
from app.models.transfer import Transfer, TransferStatus, TransferType
from app.schemas.transfer import TransferCreate, TransferResponse
from app.api.v1.auth import get_current_user
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/transfers", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
async def create_transfer(
    transfer_data: TransferCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new transfer"""
    # Validate sufficient balance
    if current_user.balance < transfer_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )
    
    # Validate receiver for internal transfers
    receiver = None
    if transfer_data.transfer_type == TransferType.INTERNAL:
        if not transfer_data.receiver_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Receiver ID is required for internal transfers"
            )
        
        result = await db.execute(select(User).where(User.id == transfer_data.receiver_id))
        receiver = result.scalar_one_or_none()
        if not receiver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receiver not found"
            )
    
    # Create transfer
    transfer = Transfer(
        reference_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
        sender_id=current_user.id,
        receiver_id=transfer_data.receiver_id,
        receiver_external_id=transfer_data.receiver_external_id,
        amount=transfer_data.amount,
        currency=transfer_data.currency,
        description=transfer_data.description,
        transfer_type=transfer_data.transfer_type,
        status=TransferStatus.COMPLETED,  # Simplified for demo
        fraud_score=0.1  # Basic fraud score
    )
    
    # Process transfer (simplified)
    current_user.balance -= transfer_data.amount
    if receiver:
        receiver.balance += transfer_data.amount
    
    db.add(transfer)
    await db.commit()
    await db.refresh(transfer)
    
    return transfer


@router.get("/transfers", response_model=List[TransferResponse])
async def get_transfers(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's transfers"""
    result = await db.execute(
        select(Transfer).where(
            (Transfer.sender_id == current_user.id) | 
            (Transfer.receiver_id == current_user.id)
        ).order_by(Transfer.created_at.desc())
    )
    transfers = result.scalars().all()
    return transfers


@router.get("/transfers/stats/summary")
async def get_transfer_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get transfer statistics for the current user"""
    # Get sent transfers
    sent_result = await db.execute(
        select(Transfer).where(Transfer.sender_id == current_user.id)
    )
    sent_transfers = sent_result.scalars().all()
    
    # Get received transfers  
    received_result = await db.execute(
        select(Transfer).where(Transfer.receiver_id == current_user.id)
    )
    received_transfers = received_result.scalars().all()
    
    total_sent = sum(t.amount for t in sent_transfers if t.status == TransferStatus.COMPLETED)
    total_received = sum(t.amount for t in received_transfers if t.status == TransferStatus.COMPLETED)
    
    return {
        "current_balance": current_user.balance,
        "total_sent": total_sent,
        "total_received": total_received,
        "total_transactions": len(sent_transfers) + len(received_transfers),
        "sent_count": len(sent_transfers),
        "received_count": len(received_transfers)
    }