from sqlalchemy import select, update
from app.database.session import AsyncSessionLocal
from app.database.models import AdminModel
from app.services.audit import log_audit_action
from app.core.logging_config import logger

async def transfer_bot_ownership(current_owner_id: int, new_owner_id: int):
    """
    نقل ملكية البوت إلى معرف مستخدم جديد وتوثيق ذلك في سجل التدقيق.
    """
    try:
        async with AsyncSessionLocal() as session:
            # التحقق مما إذا كان المستخدم الجديد مسجلاً كإداري مسبقاً، وإلا يتم إضافته
            result = await session.execute(
                select(AdminModel).where(AdminModel.user_id == new_owner_id)
            )
            admin = result.scalar_one_or_none()

            if admin:
                admin.role = "owner"
            else:
                new_admin = AdminModel(
                    user_id=new_owner_id,
                    role="owner"
                )
                session.add(new_admin)

            # خفض صلاحية المالك القديم إلى مدير (مجلد الصلاحيات)
            await session.execute(
                update(AdminModel)
                .where(AdminModel.user_id == current_owner_id)
                .values(role="manager")
            )
            
            await session.commit()

        # توثيق العملية في سجل التدقيق (Audit Log)
        await log_audit_action(
            admin_id=current_owner_id,
            action_type="TRANSFER_OWNERSHIP",
            entity_affected=f"User:{new_owner_id}",
            details=f"تم نقل ملكية البوت من المستخدم {current_owner_id} إلى المستخدم الجديد {new_owner_id}"
        )

        logger.info(f"تم نقل ملكية البوت بنجاح إلى المستخدم: {new_owner_id} بواسطة المالك السابق {current_owner_id}")
        return True, f"✅ تم نقل ملكية البوت بنجاح إلى المعرف (`{new_owner_id}`) وأصبح مالكاً رئيسياً للنظام."
    except Exception as e:
        logger.error(f"خطأ أثناء نقل ملكية البوت: {e}")
        return False, f"❌ حدث خطأ تقني أثناء نقل الملكية: {str(e)}"