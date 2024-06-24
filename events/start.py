from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.supabase import UserDatabase
from logging import Logger

logger = Logger("start.py")


def handler(app: Client):
    """
    Register the start command handler with the Telegram bot client.
    """

    @app.on_message(filters.command("start"))
    async def _(client: Client, message: Message):
        db = UserDatabase()
        telegram_id = message.from_user.id
        user = db.get_user(telegram_id)

        status = user.status if user else "NEW"

        if not user:
            db.insert_new_user(message.from_user)

        respond = response_message(status)
        await message.reply_text(respond)


def response_message(status):
    if status == "NEW":
        return "Selamat datang di CPNS Simulator Bot! Kami senang Anda bergabung dengan kami. Untuk memulai, silakan daftar dengan menggunakan perintah /register."
    elif status == "RETURNED":
        return "Selamat datang kembali di CPNS Simulator Bot! Kami senang Anda kembali. Untuk memulai lagi, silakan daftar ulang dengan menggunakan perintah /register."
    elif status == "REGISTERED":
        return "Anda sudah terdaftar di CPNS Simulator Bot. Mari kita mulai tes simulasi! Gunakan perintah /select_test untuk memilih jenis tes yang ingin Anda ambil."
    elif status == "CANCELLED":
        return "Anda telah membatalkan pendaftaran sebelumnya. Jika Anda ingin bergabung kembali, silakan daftar ulang dengan menggunakan perintah /register."
    elif status == "DELETED":
        return "Kami perhatikan Anda telah menghapus CPNS Simulator Bot sebelumnya. Jika Anda ingin kembali menggunakan layanan kami, silakan daftar ulang dengan menggunakan perintah /register. Kami senang bisa membantu Anda lagi!"
