from pyrogram import Client, filters
from pyrogram.types import Message


def handler(app: Client):
    @app.on_message(filters.command("start"))
    async def _(client: Client, message: Message):
        await message.reply_text("Welcome! The bot is running.")
