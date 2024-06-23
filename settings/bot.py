from settings.logger import BotLogger
from pyrogram import Client
from settings.config import load_config

# Initialize the logger for bot initialization
logger = BotLogger("INITIALIZATION")

def init_bot() -> Client:
    """
    Initialize and configure the Telegram bot.
    
    Returns:
        Client: Configured Telegram client.
    """
    try:
        # Load configuration from environment variables
        config = load_config()
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        raise Exception("Configuration error") from e

    try:
        # Initialize the Telegram client with the loaded configuration
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
