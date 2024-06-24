import os
from supabase import create_client, Client as SupabaseClient
from models.users import User
from pydantic import ValidationError
from pyrogram.types import User as TelegramUser
from dotenv import load_dotenv
from settings.logger import BotLogger

load_dotenv()

# Membaca URL dan KEY dari environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


class Supabase:
    def __init__(self):
        self.client: SupabaseClient = create_client(SUPABASE_URL, SUPABASE_KEY)

    def get(self, table: str, fields: str):
        return self.client.table(table).select(fields)


class UserDatabase(Supabase):
    def __init__(self):
        super().__init__()
        self.logger = BotLogger("UserDatabase")

    def get_user(self, telegram_id: int):
        self.logger.info(f"Getting user with telegram_id: {telegram_id}")
        result = (
            self.get("users", "*")
            .eq("telegram_id", telegram_id)
            .limit(1)
            .maybe_single()
            .execute()
        )
        try:
            if not result:
                raise IndexError
            return User.model_validate(result.data)
        except ValidationError as e:
            self.logger.error(f"Error while validating user: {e}")
            return None
        except IndexError:
            self.logger.info("User not found")
            return None
        except Exception:
            self.logger.error("Error while getting user")
            return None

    def insert_new_user(self, telegram_user: TelegramUser) -> User:
        telegram_id = telegram_user.id
        username = telegram_user.username
        firstname = telegram_user.first_name
        lastname = telegram_user.last_name

        try:
            new_user = User(
                telegram_id=telegram_id,
                username=username,
                firstname=firstname,
                lastname=lastname,
            ).model_dump(exclude={"id", "created_at", "email", "phone_number"})
            self.logger.info(f"New user: {new_user}")

            response = self.client.table("users").insert(new_user).execute()
            if len(response.data) == 0:
                raise Exception("No data returned")

            self.logger.info(f"New user inserted: {response}")

            return User.model_validate(response.data[0])
        except ValidationError as e:
            self.logger.error(f"Error while validating new user: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error while inserting new user: {e}")
            return None

    def register_user(self, telegram_id: int, email: str, phone_number: str = None):
        try:
            response = (
                self.client.table("users")
                .update(
                    {
                        "email": email,
                        "phone_number": phone_number,
                        "status": "REGISTERED",
                    }
                )
                .eq("telegram_id", telegram_id)
                .execute()
            )
            print(response)

            return User.model_validate(response.data[0])
        except ValidationError as e:
            self.logger.error(f"Error while validating user registration: {e}")
            return None
