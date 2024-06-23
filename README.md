# 🤖 Telegram Bot

Welcome to the **Telegram Bot** project! This bot is built using the [Pyrogram](https://pyrogram.org/) library and includes basic commands like `/start` and `/help`. It is designed to be easily extendable and comes with robust logging for easy monitoring and debugging.

## ✨ Features

- 🚀 **Start Command**: Responds to the `/start` command.
- 📖 **Help Command**: Responds to the `/help` command.
- 🛠️ **Modular Event Handling**: Easily add new commands by creating new modules in the `events` directory.
- 📋 **Custom Logging**: Logs bot activities and errors for easier debugging and monitoring.

## 🛠️ Installation

1. **Clone the repository:**
    ```sh
    https://github.com/erzawansyah/pyrogram_telebot.git
    cd pyrogram_telebot
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    - Create a `.env` file in the root directory of your project.
    - Copy the contents of `.env.example` to `.env` and replace `API_ID`, `API_HASH`, and `BOT_TOKEN` with your actual values.
    ```env
    TELEGRAM_APP_API_ID=API_ID # Replace API_ID with your own API_ID. You can get it from https://my.telegram.org
    TELEGRAM_APP_API_HASH=API_HASH # Replace API_HASH with your own API_HASH. You can get it from https://my.telegram.org
    TELEGRAM_BOT_TOKEN=BOT_TOKEN # Replace BOT_TOKEN with your own BOT_TOKEN. You can get it from https://t.me/botfather
    ```

## 🚀 Usage

1. **Run the bot:**
    ```sh
    python main.py
    ```

2. **Interacting with the bot:**
    - Send `/start` to the bot to receive a welcome message.
    - Send `/help` to get help information.

## 📂 Project Structure

```plaintext
├── .env.example
├── main.py
├── requirements.txt
├── settings
│   ├── bot.py
│   ├── config.py
│   ├── event_handler.py
│   ├── logger.py
├── events
│   ├── help.py
│   └── start.py
├── .env.example**: Example environment variables file.
├── main.py**: Entry point of the bot.
├── requirements.txt**: List of dependencies.
├── settings/**: Contains configuration, bot initialization, event handling, and logging logic.
├── events/**: Contains command handlers for the bot.
```

## ➕ Adding New Commands

To add a new command to the bot:

1. **Create a new Python file in the `events` directory**:
    ```python
    # events/new_command.py
    from pyrogram import Client, filters

    def handler(app: Client):
        @app.on_message(filters.command("newcommand"))
        async def _(client, message):
            await message.reply_text("This is a response to the new command.")
    ```

2. **Register the new command in `main.py`**:
    ```python
    # main.py
    handler.register(
        EventHandlerType(
            filename="new_command",
            description="New command",
        )
    )
    ```

## 📋 Logging

The bot uses a custom logger for logging events. Logs include informational messages and error reports, which help in monitoring the bot's performance and debugging issues.  Here’s an example of how logging is implemented in this bot:

```python
from settings.logger import BotLogger

# Initialize the logger
logger = BotLogger("app")

# Log information when the bot starts
logger.info("Starting the bot")

# Log an error if there is an issue
try:
    app.run()
except Exception as e:
    logger.error(f"Error occurred: {e}")
```

## 📚 Detailed Documentation

For more detailed information, please refer to the [📖 API Documentation](docs.md)


## 🤝 Contributing

If you wish to contribute to this project, feel free to fork the repository and submit a pull request. Ensure that your code adheres to the existing coding standards and is well-documented.


## 🌐 Social Links

Follow us on:
- [GitHub](https://github.com/erzawansyah)
- [Twitter](https://twitter.com/erzawansyah)
- [LinkedIn](https://linkedin.com/in/erzawansyah)

## ☁️ Hosting

This bot can be hosted on various platforms. We recommend [Hostinger](https://hostinger.com?REFERRALCODE=1MUHAMADERZ73) for reliable and affordable hosting. Use our [referral link](https://hostinger.com?REFERRALCODE=1MUHAMADERZ73) to get a discount and support our project!

## ⚠️ Disclaimer

This README file was generated with the assistance of [GitHub README on ChatGPT](https://chatgpt.com/g/g-rA63DaENC-github-readme) by [Sourceduty](https://github.com/sourceduty). While efforts have been made to ensure the accuracy and completeness of the information provided, please review and verify all details to ensure they meet your project's requirements.

---

Made with ❤️ by [@erzawansyah](https://github.com/erzawansyah)
