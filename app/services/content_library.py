from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.database.models import ContentItemModel, AdhkarModel
from app.core.logging_config import logger

async def add_content_item(category: str, title: str, body: str, reference: str = None) -> bool:
    """
    إضافة عنصر جديد إلى مكتبة المحتوى الإسلامي.
    """
    try:
        async with AsyncSessionLocal() as session:
            new_item = ContentItemModel(
                category=category,
                title=title,
                body=body,
                reference=reference
            )
            session.add(new_item)
            await session.commit()
            logger.info(f"تمت إضافة محتوى جديد بعنوان: {title} في تصنيف {category}")
            return True
    except Exception as e:
        logger.error(f"خطأ أثناء إضافة عنصر لمكتبة المحتوى: {e}")
        return False

async def get_content_by_category(category: str):
    """
    جلب العناصر التابعة لتصنيف معين من مكتبة المحتوى.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ContentItemModel).where(ContentItemModel.category == category)
        )
        return result.scalars().all()

async def get_adhkar_list(adhkar_type: str):
    """
    جلب أذكار الصباح أو المساء.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(AdhkarModel).where(AdhkarModel.type == adhkar_type, AdhkarModel.is_active == True)
        )
        return result.scalars().all()