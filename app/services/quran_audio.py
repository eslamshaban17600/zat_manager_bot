from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.database.models import ReciterModel, ListeningPlanModel
from app.core.logging_config import logger

async def add_reciter(full_name: str, display_name: str, biography: str = None) -> bool:
    """
    إضافة قارئ جديد إلى نظام الختمات السماعية.
    """
    try:
        async with AsyncSessionLocal() as session:
            new_reciter = ReciterModel(
                full_name=full_name,
                display_name=display_name,
                biography=biography
            )
            session.add(new_reciter)
            await session.commit()
            logger.info(f"تمت إضافة القارئ بنجاح: {display_name}")
            return True
    except Exception as e:
        logger.error(f"خطأ أثناء إضافة القارئ: {e}")
        return False

async def get_all_reciters():
    """
    جلب قائمة القراء المتاحين في النظام.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(ReciterModel))
        return result.scalars().all()