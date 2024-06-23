import importlib
from pyrogram import Client
from settings.logger import BotLogger
from pydantic import BaseModel
from typing import Optional


class EventHandlerType(BaseModel):
    filename: str
    description: Optional[str] = None


class EventHandler:

    def __init__(
        self,
        client: Client,
        logger: BotLogger = BotLogger("EVENT_HANDLER"),
    ):
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
