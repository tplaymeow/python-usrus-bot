from abc import ABC

from motor.motor_asyncio import AsyncIOMotorClient


class AbstractRepository(ABC):
    def __init__(self, client: AsyncIOMotorClient) -> None:
        self.database = client["bot_database"]
