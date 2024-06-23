from settings.bot import init_bot as bot_initialization
from settings.logger import BotLogger
from settings.event_handler import EventHandler, EventHandlerType

# Initialize the bot and logger
logger = BotLogger("app")
app = bot_initialization()

# Initialize the event controller
handler = EventHandler(app)

handler.register(
    EventHandlerType(
        filename="help",
        description="Help command",
    )
)
handler.register(
    EventHandlerType(
        filename="start",
        description="Start command",
    )
)

if __name__ == "__main__":
    handler.load()
    logger.info("Starting the bot")
    logger.info("Bot is running")
    app.run()
