from app.database.session import AsyncSessionLocal
from app.database.models import AuditLogModel
from app.core.logging_config import logger

async def log_audit_action(admin_id: int, action_type: str, entity_affected: str = None, details: str = None):
    """
    تسجيل العمليات الإدارية في سجل التدقيق (Audit Log) المستقل.
    """
    try:
        async with AsyncSessionLocal() as session:
            log_entry = AuditLogModel(
                admin_id=admin_id,
                action_type=action_type,
                entity_affected=entity_affected,
                result="SUCCESS",
                details=details
            )
            session.add(log_entry)
            await session.commit()
    except Exception as e:
        logger.error(f"خطأ أثناء تسجيل التدقيق: {e}")