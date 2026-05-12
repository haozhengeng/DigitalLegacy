from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.trigger_config import TriggerConfig
from app.models.trigger_log import TriggerLog
from app.schemas.trigger import (
    TriggerConfigUpdate, TriggerConfigResponse,
    CheckInResponse, TriggerLogResponse,
    EmergencyRecallResponse, TriggerStatusResponse,
)
from app.core.deps import get_current_user

router = APIRouter(prefix="/trigger", tags=["Dead Man's Switch"])


@router.get("/config", response_model=TriggerConfigResponse)
async def get_config(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TriggerConfig).where(TriggerConfig.user_id == current_user.id)
    )
    config = result.scalar_one_or_none()
    if not config:
        config = TriggerConfig(user_id=current_user.id)
        db.add(config)
        await db.commit()
        await db.refresh(config)
    return TriggerConfigResponse.model_validate(config)


@router.put("/config", response_model=TriggerConfigResponse)
async def update_config(
    data: TriggerConfigUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TriggerConfig).where(TriggerConfig.user_id == current_user.id)
    )
    config = result.scalar_one_or_none()
    if not config:
        config = TriggerConfig(user_id=current_user.id)
        db.add(config)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(config, key, value)
    await db.commit()
    await db.refresh(config)
    return TriggerConfigResponse.model_validate(config)


@router.post("/check-in", response_model=CheckInResponse)
async def check_in(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    now = datetime.utcnow()
    result = await db.execute(
        select(TriggerConfig).where(TriggerConfig.user_id == current_user.id)
    )
    config = result.scalar_one_or_none()
    if not config:
        config = TriggerConfig(user_id=current_user.id)
        db.add(config)

    config.last_check_in = now
    config.is_triggered = False
    config.trigger_started_at = None

    log = TriggerLog(user_id=current_user.id, event_type="check_in", description="User checked in")
    db.add(log)
    await db.commit()

    return CheckInResponse(message="安全打卡成功，系统已重置计时", last_check_in=now)


@router.get("/status", response_model=TriggerStatusResponse)
async def get_trigger_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TriggerConfig).where(TriggerConfig.user_id == current_user.id)
    )
    config = result.scalar_one_or_none() or TriggerConfig(user_id=current_user.id)

    now = datetime.utcnow()
    days_since = 999
    if config.last_check_in:
        days_since = (now - config.last_check_in).days

    stage = "守护期"
    next_alert = None
    if config.is_emergency_recalled:
        stage = "已紧急撤回"
    elif config.is_triggered:
        triggered_days = (now - config.trigger_started_at).days if config.trigger_started_at else 0
        if triggered_days <= 3:
            stage = f"预警期 (T+{triggered_days}d) - 即将发送提醒"
        elif triggered_days <= 7:
            stage = f"预警期 (T+{triggered_days}d) - 将联系紧急联系人"
        else:
            stage = "交付期 - 信息正在分发"
    elif config.last_check_in is None:
        stage = "守护期 - 尚未打卡"
        next_alert = "请尽快完成首次安全打卡"
    elif days_since >= config.inactivity_days:
        remaining = days_since - config.inactivity_days
        stage = f"预警期 (T+{remaining}d)"
    else:
        remaining = config.inactivity_days - days_since
        next_alert = f"{remaining} 天后进入预警期"

    return TriggerStatusResponse(
        is_triggered=config.is_triggered,
        is_emergency_recalled=config.is_emergency_recalled,
        days_since_last_checkin=days_since,
        inactivity_days=config.inactivity_days,
        trigger_stage=stage,
        next_alert_at=next_alert,
    )


@router.post("/emergency-recall", response_model=EmergencyRecallResponse)
async def emergency_recall(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TriggerConfig).where(TriggerConfig.user_id == current_user.id)
    )
    config = result.scalar_one_or_none()
    if not config:
        config = TriggerConfig(user_id=current_user.id)
        db.add(config)

    config.is_emergency_recalled = True
    config.is_triggered = False
    config.last_check_in = datetime.utcnow()
    config.trigger_started_at = None

    log = TriggerLog(user_id=current_user.id, event_type="emergency_recall", description="User triggered emergency recall")
    db.add(log)
    await db.commit()

    return EmergencyRecallResponse(message="已紧急撤回，所有触发流程已终止", is_emergency_recalled=True)


@router.get("/logs", response_model=List[TriggerLogResponse])
async def get_logs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TriggerLog).where(TriggerLog.user_id == current_user.id)
        .order_by(TriggerLog.created_at.desc()).limit(50)
    )
    return [TriggerLogResponse.model_validate(l) for l in result.scalars().all()]
