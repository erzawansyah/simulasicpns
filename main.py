from settings.bot import init_bot as bot_initialization
from settings.logger import BotLogger
from settings.event_handler import EventHandler, EventHandlerType

# Initialize the logger for the bot
logger = BotLogger("app")

# Initialize the bot using the configuration settings
app = bot_initialization()

# Create an event handler for the bot
handler = EventHandler(app)

# Register the help command with the event handler
handler.register(
    EventHandlerType(
        filename="register",
        description="Register command",
    )
)

# Register the start command with the event handler
handler.register(
    EventHandlerType(
        filename="start",
        description="Start command",
    )
)

if __name__ == "__main__":
    # Load and run the bot
    handler.load()
    logger.info("Starting the bot")
    logger.info("Bot is running")
    app.run()
