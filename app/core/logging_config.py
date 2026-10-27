import logging
import sys
from pathlib import Path
from app.core.config import settings

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "bot_execution.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    # تقليل إزعاج سجلات مكتبات الطرف الثالث
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("apscheduler").setLevel(logging.WARNING)

logger = logging.getLogger("ZatBot")