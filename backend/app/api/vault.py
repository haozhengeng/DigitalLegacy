from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.vault_item import VaultItem
from app.schemas.vault import VaultItemCreate, VaultItemUpdate, VaultItemResponse
from app.core.deps import get_current_user

router = APIRouter(prefix="/vault", tags=["Vault"])


@router.get("/", response_model=List[VaultItemResponse])
async def list_items(
    category: str = Query("", description="Filter by category"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(VaultItem).where(VaultItem.user_id == current_user.id)
    if category:
        query = query.where(VaultItem.category == category)
    query = query.order_by(VaultItem.importance.desc(), VaultItem.created_at.desc())
    result = await db.execute(query)
    return [VaultItemResponse.model_validate(item) for item in result.scalars().all()]


@router.post("/", response_model=VaultItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    data: VaultItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    item = VaultItem(**data.model_dump(exclude={"encrypted_content"}), user_id=current_user.id)
    item.encrypted_content = data.encrypted_content
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return VaultItemResponse.model_validate(item)


@router.get("/{item_id}", response_model=VaultItemResponse)
async def get_item(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(VaultItem).where(VaultItem.id == item_id, VaultItem.user_id == current_user.id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return VaultItemResponse.model_validate(item)


@router.put("/{item_id}", response_model=VaultItemResponse)
async def update_item(
    item_id: str,
    data: VaultItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(VaultItem).where(VaultItem.id == item_id, VaultItem.user_id == current_user.id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    await db.commit()
    await db.refresh(item)
    return VaultItemResponse.model_validate(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(VaultItem).where(VaultItem.id == item_id, VaultItem.user_id == current_user.id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    await db.delete(item)
    await db.commit()
