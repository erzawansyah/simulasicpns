from settings.logger import BotLogger
from pyrogram import Client
from settings.config import load_config

logger = BotLogger("INITIALIZATION")


def init_bot() -> Client:
    try:
        config = load_config()
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        raise Exception("Configuration error") from e

    try:
        app = Client(
            "telebot_dev",
            api_id=config.api_id,
            api_hash=config.api_hash,
            bot_token=config.bot_token,
        )
        logger.info("Bot initialized successfully")
        return app
    except Exception as e:
        logger.error(f"Bot initialization error: {e}")
        raise Exception("Bot initialization error") from e
