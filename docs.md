### Telegram Bot Documentation

This documentation will guide you through the setup and usage of your Telegram bot. The bot uses the Pyrogram library and requires specific environment variables for configuration. This guide assumes you have basic knowledge of Python and virtual environments.

#### Table of Contents
- [Telegram Bot Documentation](#telegram-bot-documentation)
  - [Table of Contents](#table-of-contents)
- [Environment Setup](#environment-setup)
- [Project Structure](#project-structure)
- [Dependencies Installation](#dependencies-installation)
- [Bot Initialization](#bot-initialization)
- [Configuration](#configuration)
- [Event Handling](#event-handling)
- [Running the Bot](#running-the-bot)
- [Event Handlers](#event-handlers)
  - [`events/start.py`](#eventsstartpy)
  - [`events/help.py`](#eventshelppy)
- [Conclusion](#conclusion)

### Environment Setup

Before running the bot, you need to set up the required environment variables. Create a `.env` file in your project root directory with the following content:

```
TELEGRAM_APP_API_ID=API_ID # Replace API_ID with your own API_ID from https://my.telegram.org
TELEGRAM_APP_API_HASH=API_HASH # Replace API_HASH with your own API_HASH from https://my.telegram.org
TELEGRAM_BOT_TOKEN=BOT_TOKEN # Replace BOT_TOKEN with your own BOT_TOKEN from https://t.me/botfather
```

### Project Structure

The project is organized as follows:

```
.
├── .env
├── main.py
├── requirements.txt
├── settings/
│   ├── bot.py
│   ├── config.py
│   ├── event_handler.py
│   ├── logger.py
└── events/
    ├── start.py
    └── help.py
```

### Dependencies Installation

Ensure you have `pip` installed. You can install the required dependencies using the `requirements.txt` file. First, create a virtual environment and activate it:

```sh
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

Next, install the dependencies:

```sh
pip install -r requirements.txt
```

Here is the `requirements.txt` content:

```
annotated-types==0.7.0
pyaes==1.6.1
pydantic==2.7.4
pydantic_core==2.18.4
Pyrogram==2.0.106
PySocks==1.7.1
python-dotenv==1.0.1
TgCrypto==1.2.5
typing_extensions==4.12.2
```

### Bot Initialization

The bot initialization is handled in `settings/bot.py`. The `init_bot` function initializes the Pyrogram `Client` with the API credentials and bot token.

```python
from pyrogram import Client
from settings.config import load_config
from settings.logger import BotLogger

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
```

### Configuration

The bot configuration is managed in `settings/config.py` using the `pydantic` library for validation and `python-dotenv` to load environment variables.

```python
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from settings.logger import BotLogger

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
```

### Event Handling

The event handling mechanism is implemented in `settings/event_handler.py`. It allows registering and loading event handlers dynamically.

```python
import importlib
from pyrogram import Client
from pydantic import BaseModel
from typing import Optional
from settings.logger import BotLogger

class EventHandlerType(BaseModel):
    filename: str
    description: Optional[str] = None

class EventHandler:
    def __init__(self, client: Client, logger: BotLogger = BotLogger("EVENT_HANDLER")):
        self.client = client
        self.logger = logger
        self.events = []

    def __execute(self, module, filename: str):
        if hasattr(module, "handler"):
            self.logger.info(f"Loaded event: {filename}.py")
            handler = getattr(module, "handler")
            handler(self.client)
        else:
            raise ImportError(f"No function named 'handler' in {filename}.py")

    def __event_handler(self, filename: str):
        try:
            module_name = f"events.{filename}"
            module = importlib.import_module(module_name)
            self.__execute(module, filename)
        except Exception as e:
            self.logger.error(f"Failed to load event: {e}")

    def register(self, event: EventHandlerType):
        self.events.append(event)

    def load(self):
        for event in self.events:
            self.__event_handler(event.filename)
```

### Running the Bot

The main script `main.py` initializes the bot and event handler, registers the events, and starts the bot.

```python
from settings.bot import init_bot as bot_initialization
from settings.logger import BotLogger
from settings.event_handler import EventHandler, EventHandlerType

logger = BotLogger("app")
app = bot_initialization()

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
    app.run()
```

### Event Handlers

The bot includes two basic event handlers: `start` and `help`.

#### `events/start.py`

Handles the `/start` command.

```python
from pyrogram import Client, filters

def handler(app: Client):
    @app.on_message(filters.command("start"))
    async def start(client, message):
        await message.reply_text("Welcome! This is the start message.")
```

#### `events/help.py`

Handles the `/help` command.

```python
from pyrogram import Client, filters

def handler(app: Client):
    @app.on_message(filters.command("help"))
    async def help(client, message):
        await message.reply_text("This is a help message.")
```

### Conclusion

You now have a fully functional Telegram bot with a modular event handling system. Ensure that your environment variables are correctly set up in the `.env` file before running the bot. Use `main.py` to start the bot, and it will respond to the `/start` and `/help` commands as defined in the event handlers.
