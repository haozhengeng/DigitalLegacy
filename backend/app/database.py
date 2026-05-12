from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """SQLAlchemy 声明式基类，所有模型继承此类"""
    pass


async def get_db():
    """FastAPI 依赖注入：获取异步数据库会话"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """初始化数据库：导入所有模型并创建表结构"""
    from app.models.user import User
    from app.models.vault_item import VaultItem
    from app.models.emotional_file import EmotionalFile
    from app.models.key_fragment import KeyFragment
    from app.models.beneficiary import Beneficiary
    from app.models.trigger_config import TriggerConfig
    from app.models.trigger_log import TriggerLog
    from app.models.delivery_log import DeliveryLog
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
