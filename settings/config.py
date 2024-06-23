import os
from settings.logger import BotLogger
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

logger = BotLogger("CONFIG")


class BotConfig(BaseModel):
    api_id: str
    api_hash: str
    bot_token: str


def load_config() -> BotConfig:
    load_dotenv()
    try:
        config = BotConfig(
            api_id=os.environ["TELEGRAM_APP_API_ID"],
            api_hash=os.environ["TELEGRAM_APP_API_HASH"],
            bot_token=os.environ["TELEGRAM_BOT_TOKEN"],
        )
        logger.info("Configuration loaded successfully")
        return config
    except KeyError as e:
        logger.error(f"Missing environment variable: {e}")
        raise
    except ValidationError as e:
        logger.error(f"Configuration validation error: {e}")
        raise
