import logging
import logging.config
from datetime import datetime

from ImageClassifier import settings_dir
from settings.config import Config


def setup_logging():
    """Load logging configuration"""

    config = "logging.ini"
    config_path = settings_dir / config

    timestamp = datetime.now().strftime("%Y%m%d-%H:%M:%S")

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logging": f"{Config.LOG_DIR}/{timestamp}.log"},
    )