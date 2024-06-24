from pydantic import BaseModel
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ForceReply
from plugins.supabase import UserDatabase
from models.users import UserStatus
from typing import Literal
import re
from settings.logger import BotLogger

logger = BotLogger("register.py")


class Model(BaseModel):
    step: Literal["step1", "step2", "step3", "step4"] = "step1"
    email: str = None
    phone: str = None

    """A class to handle the registration process of a user.
    step: str = The current state of the registration process.
    it can be either "step1", "step2", "step3", or "step4".
    step1: The user is asked if they want to provide an email.
    step2: The user will provide their email.
    step3: The user will asked if they want to provide their phone number.
    step4: The registration process is completed.

    email: str = The email of the user. (default: None)
    phone: str = The phone number of the user. (default: None)
    """


class Validation(BaseModel):
    status: bool
    message: str | None = None


class StepHandler:
    def __init__(self):
        self.data: dict[int, Model] = {}

    def user_exists(self, telegram_id: int):
        return telegram_id in self.data

    def assign(self, telegram_id: int):
        self.data[telegram_id] = Model(step="step1")

    def update(self, telegram_id: int, **kwargs):
        for key, value in kwargs.items():
            setattr(self.data[telegram_id], key, value)

    def get(self, telegram_id: int, key: str):
        return getattr(self.data[telegram_id], key)

    def register_user(self, telegram_id: int, email: str, phone: str = None):
        db = UserDatabase()
        user = db.get_user(telegram_id)
        if user:
            user.email = email
            user.status = UserStatus.REGISTERED
            if phone:
                user.phone_number = phone
            db.register_user(telegram_id, email, phone)

    def start(self, msg: Message):
        """Mengecek apakah pengguna dapat memulai proses pendaftaran."""
        user = UserDatabase().get_user(msg.from_user.id)
        if not user:
            return Validation(
                status=False,
                message="Anda belum memulai bot. Gunakan perintah /start terlebih dahulu.",
            )
        if user.status == UserStatus.REGISTERED:
            return Validation(
                status=False,
                message="Anda sudah terdaftar. Gunakan perintah /select_test untuk memilih jenis tes yang ingin Anda ambil.",
            )
        if msg.from_user.id in self.data:
            return Validation(
                status=False,
                message="Anda sudah dalam proses registrasi. Silakan selesaikan terlebih dahulu.",
            )
        self.assign(msg.from_user.id)
        return Validation(status=True)

    def step1_action(self, msg: Message):
        """Menanyakan kesediaan pengguna untuk memberikan email sebagai bagian dari proses pendaftaran."""
        markup = ReplyKeyboardMarkup(
            [[KeyboardButton("Tidak")], [KeyboardButton("Ya")]],
            one_time_keyboard=True,
            resize_keyboard=True,
        )
        return msg.reply_text(
            "Pendaftaran ini memerlukan email Anda. Apakah Anda bersedia memberikan email Anda?",
            reply_markup=markup,
        )

    def step1_validation(self, msg: Message):
        """Mengecek apakah pengguna memilih 'Ya' atau 'Tidak' saat diminta memberikan email."""
        if msg.text.lower() not in ["ya", "tidak"]:
            return Validation(status=False, message="Mohon pilih 'Ya' atau 'Tidak'.")
        if msg.text.lower() == "tidak":
            del self.data[msg.from_user.id]
            return Validation(status=False, message="Pendaftaran dibatalkan.")
        if msg.text.lower() == "ya" and self.data[msg.from_user.id].email:
            return Validation(
                status=False,
                message="Anda sudah memberikan email. Lanjutkan ke langkah berikutnya.",
            )
        self.update(msg.from_user.id, step="step2")
        return Validation(status=True)

    def step2_action(self, msg: Message):
        """Meminta pengguna untuk memberikan email mereka."""
        return msg.reply_text(
            "Silakan masukkan email Anda:",
            reply_markup=ForceReply(selective=True),
        )

    def step2_validation(self, msg: Message):
        """Memvalidasi email yang dimasukkan oleh pengguna."""
        email = msg.text.strip()  # Remove leading and trailing whitespaces
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return Validation(
                status=False,
                message="Email yang dimasukkan tidak valid. Silakan masukkan email yang benar.",
            )
        self.update(msg.from_user.id, email=email, step="step3")
        return Validation(status=True)

    def step3_action(self, msg: Message):
        """Menanyakan kesediaan pengguna untuk memberikan nomor telepon mereka."""
        markup = ReplyKeyboardMarkup(
            [[KeyboardButton("Tidak")], [KeyboardButton("Ya")]],
            one_time_keyboard=True,
            resize_keyboard=True,
        )
        return msg.reply_text(
            "Apakah Anda bersedia nomor telepon Anda disimpan? Anda tetap bisa menggunakan bot tanpa memberikan nomor telepon.",
            reply_markup=markup,
        )

    def step3_validation(self, msg: Message):
        """Memvalidasi respon pengguna saat diminta memberikan nomor telepon."""
        if msg.text.lower() not in ["ya", "tidak"]:
            return Validation(status=False, message="Mohon pilih 'Ya' atau 'Tidak'.")
        if msg.text.lower() == "tidak":
            self.update(msg.from_user.id, step="step4")
            return Validation(status=True, message="tidak")
        if msg.text.lower() == "ya" and (
            not msg.from_user.phone_number
            or msg.from_user.phone_number == "0"
            or msg.from_user.phone_number == ""
            or msg.from_user.phone_number is None
        ):
            self.update(msg.from_user.id, step="step4")
            return Validation(status=True, message="kosong")
        self.update(msg.from_user.id, step="step4", phone=msg.from_user.phone_number)
        return Validation(status=True, message=msg.text.lower())

    def step4_action(self, msg: Message, status: str):
        """Menyelesaikan proses pendaftaran pengguna."""
        email = self.get(msg.from_user.id, "email")
        phone_number = self.get(msg.from_user.id, "phone")
        self.register_user(msg.from_user.id, email, phone_number)
        del self.data[msg.from_user.id]

        if status in ["tidak", "kosong"]:
            return msg.reply_text(
                "Terima kasih telah mendaftar. Anda bisa memulai tes simulasi dengan menggunakan perintah /select_test."
            )
        return msg.reply_text(
            "Terima kasih telah mendaftar. Anda bisa memulai tes simulasi dengan menggunakan perintah /select_test."
        )


on_register = StepHandler()


def handler(app: Client):
    """
    Register the register command handler with the Telegram bot client.
    """

    # Ketika pengguna memulai proses pendaftaran
    @app.on_message(filters.command("register"))
    async def _(_, message: Message):
        validation = on_register.start(message)
        if not validation.status:
            await message.reply_text(validation.message)
        else:
            await on_register.step1_action(message)

    # Menangani respon pengguna selama proses pendaftaran
    @app.on_message(
        filters.text
        & filters.create(lambda _, __, m: on_register.user_exists(m.from_user.id))
    )
    async def __(_, message: Message):
        current_step = on_register.get(message.from_user.id, "step")
        if current_step == "step1":
            is_valid = on_register.step1_validation(message)
            if not is_valid.status:
                await message.reply_text(is_valid.message)
            else:
                await on_register.step2_action(message)
        elif current_step == "step2":
            is_valid = on_register.step2_validation(message)
            if not is_valid.status:
                await message.reply_text(is_valid.message)
            else:
                await on_register.step3_action(message)
        elif current_step == "step3":
            is_valid = on_register.step3_validation(message)
            if not is_valid.status:
                await message.reply_text(is_valid.message)
            else:
                await on_register.step4_action(message, is_valid.message)
        else:
            await message.reply_text(
                "Anda belum memulai proses pendaftaran. Gunakan perintah /register terlebih dahulu."
            )
