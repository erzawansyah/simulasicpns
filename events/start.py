from pyrogram import Client, filters

def handler(app: Client):
    """
    Register the start command handler with the Telegram bot client.
    
    Args:
        app (Client): The Telegram bot client.
    """
    @app.on_message(filters.command("start"))
    async def _(client, message):
        await message.reply_text("This is a start message.")
