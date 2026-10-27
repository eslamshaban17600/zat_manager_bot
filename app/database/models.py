import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from app.database.session import Base

class AdminModel(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False) # معرف المستخدم في تيليجرام
    role = Column(String(50), default="editor") # يمكن أن يكون: 'owner' أو 'manager' أو 'editor'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
class ChannelModel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    username = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    timezone = Column(String(50), default="Africa/Cairo")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ScheduledJobModel(Base):
    __tablename__ = "scheduled_jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String(100), nullable=False)
    job_type = Column(String(50), nullable=False)
    payload = Column(Text, nullable=False) # JSON or text data
    cron_expression = Column(String(100), nullable=True)
    run_date = Column(DateTime, nullable=True)
    is_paused = Column(Boolean, default=False)
    next_run_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ContentItemModel(Base):
    __tablename__ = "content_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    reference = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AuditLogModel(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, nullable=False)
    action_type = Column(String(100), nullable=False)
    entity_affected = Column(String(100), nullable=True)
    result = Column(String(50), default="SUCCESS")
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ReciterModel(Base):
    __tablename__ = "reciters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=False)
    biography = Column(Text, nullable=True)
    source_url = Column(String(255), nullable=True)

class ListeningPlanModel(Base):
    __tablename__ = "listening_plans"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String(100), nullable=False)
    reciter_id = Column(Integer, ForeignKey("reciters.id"), nullable=False)
    plan_type = Column(String(50), default="full_quran")
    current_position = Column(String(100), default="Surah Al-Fatihah")
    is_active = Column(Boolean, default=True)