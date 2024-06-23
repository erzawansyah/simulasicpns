# Telegram Bot Documentation

This document provides a brief overview and practical guide for setting up and using your Telegram bot. For detailed documentation, refer to the `docs.md` file.

## Table of Contents
- [Telegram Bot Documentation](#telegram-bot-documentation)
  - [Table of Contents](#table-of-contents)
  - [Environment Setup](#environment-setup)
  - [Project Structure](#project-structure)
  - [Dependencies Installation](#dependencies-installation)
  - [Running the Bot](#running-the-bot)
  - [Adding New Events](#adding-new-events)
  - [Detailed Documentation](#detailed-documentation)

## Environment Setup

Create a `.env` file in your project root directory with the following content:

```
TELEGRAM_APP_API_ID=API_ID # Replace with your API_ID from https://my.telegram.org
TELEGRAM_APP_API_HASH=API_HASH # Replace with your API_HASH from https://my.telegram.org
TELEGRAM_BOT_TOKEN=BOT_TOKEN # Replace with your BOT_TOKEN from https://t.me/botfather
```

## Project Structure

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

## Dependencies Installation

Set up a virtual environment and install dependencies:

```sh
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Running the Bot

Start your bot by running:

```sh
python main.py
```

## Adding New Events

1. **Create a new event handler**: Add a new file in the `events` directory, e.g., `events/echo.py`.

2. **Define the handler**:
    ```python
    from pyrogram import Client, filters

    def handler(app: Client):
        @app.on_message(filters.command("echo"))
        async def echo(client, message):
            await message.reply_text(message.text)
    ```

3. **Register the event**: Update `main.py` to register the new event.
    ```python
    handler.register(
        EventHandlerType(
            filename="echo",
            description="Echo command",
        )
    )
    ```

## Detailed Documentation

For more detailed information, please refer to the [API Documentation](docs.md)
