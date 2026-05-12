from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.beneficiary import Beneficiary
from app.schemas.beneficiary import BeneficiaryCreate, BeneficiaryUpdate, BeneficiaryResponse, BeneficiaryVerify
from app.core.deps import get_current_user

router = APIRouter(prefix="/beneficiaries", tags=["Beneficiaries"])


@router.get("/", response_model=List[BeneficiaryResponse])
async def list_beneficiaries(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Beneficiary).where(Beneficiary.user_id == current_user.id)
        .order_by(Beneficiary.created_at.desc())
    )
    return [BeneficiaryResponse.model_validate(b) for b in result.scalars().all()]


@router.post("/", response_model=BeneficiaryResponse, status_code=status.HTTP_201_CREATED)
async def create_beneficiary(
    data: BeneficiaryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    beneficiary = Beneficiary(**data.model_dump(), user_id=current_user.id)
    db.add(beneficiary)
    await db.commit()
    await db.refresh(beneficiary)
    return BeneficiaryResponse.model_validate(beneficiary)


@router.put("/{beneficiary_id}", response_model=BeneficiaryResponse)
async def update_beneficiary(
    beneficiary_id: str,
    data: BeneficiaryUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Beneficiary).where(Beneficiary.id == beneficiary_id, Beneficiary.user_id == current_user.id)
    )
    b = result.scalar_one_or_none()
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(b, key, value)
    await db.commit()
    await db.refresh(b)
    return BeneficiaryResponse.model_validate(b)


@router.post("/{beneficiary_id}/verify", response_model=BeneficiaryResponse)
async def verify_beneficiary(
    beneficiary_id: str,
    data: BeneficiaryVerify,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Beneficiary).where(Beneficiary.id == beneficiary_id, Beneficiary.user_id == current_user.id)
    )
    b = result.scalar_one_or_none()
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary not found")
    b.id_number = data.id_number
    b.is_identity_verified = True
    await db.commit()
    await db.refresh(b)
    return BeneficiaryResponse.model_validate(b)


@router.delete("/{beneficiary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_beneficiary(
    beneficiary_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Beneficiary).where(Beneficiary.id == beneficiary_id, Beneficiary.user_id == current_user.id)
    )
    b = result.scalar_one_or_none()
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary not found")
    await db.delete(b)
    await db.commit()
