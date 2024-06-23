from pyrogram import Client, filters


def handler(app: Client):
    @app.on_message(filters.command("help"))
    async def _(client, message):
        await message.reply_text("This is a help message.")
