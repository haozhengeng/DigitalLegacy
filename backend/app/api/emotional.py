from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.emotional_file import EmotionalFile
from app.schemas.emotional import EmotionalFileCreate, EmotionalFileUpdate, EmotionalFileResponse
from app.core.deps import get_current_user

router = APIRouter(prefix="/emotional", tags=["Emotional Files"])


@router.get("/", response_model=List[EmotionalFileResponse])
async def list_files(
    file_type: str = "",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取情感档案列表，支持按类型筛选"""
    query = select(EmotionalFile).where(EmotionalFile.user_id == current_user.id)
    if file_type:
        query = query.where(EmotionalFile.file_type == file_type)
    query = query.order_by(EmotionalFile.created_at.desc())
    result = await db.execute(query)
    return [EmotionalFileResponse.model_validate(f) for f in result.scalars().all()]


@router.post("/", response_model=EmotionalFileResponse, status_code=status.HTTP_201_CREATED)
async def create_file(
    data: EmotionalFileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """创建情感档案（信件/语音/视频等）"""
    ef = EmotionalFile(**data.model_dump(), user_id=current_user.id)
    db.add(ef)
    await db.commit()
    await db.refresh(ef)
    return EmotionalFileResponse.model_validate(ef)


@router.get("/{file_id}", response_model=EmotionalFileResponse)
async def get_file(
    file_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取单个情感档案详情"""
    result = await db.execute(
        select(EmotionalFile).where(EmotionalFile.id == file_id, EmotionalFile.user_id == current_user.id)
    )
    ef = result.scalar_one_or_none()
    if not ef:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return EmotionalFileResponse.model_validate(ef)


@router.put("/{file_id}", response_model=EmotionalFileResponse)
async def update_file(
    file_id: str,
    data: EmotionalFileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """更新情感档案"""
    result = await db.execute(
        select(EmotionalFile).where(EmotionalFile.id == file_id, EmotionalFile.user_id == current_user.id)
    )
    ef = result.scalar_one_or_none()
    if not ef:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ef, key, value)
    await db.commit()
    await db.refresh(ef)
    return EmotionalFileResponse.model_validate(ef)


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """删除情感档案"""
    result = await db.execute(
        select(EmotionalFile).where(EmotionalFile.id == file_id, EmotionalFile.user_id == current_user.id)
    )
    ef = result.scalar_one_or_none()
    if not ef:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    await db.delete(ef)
    await db.commit()
