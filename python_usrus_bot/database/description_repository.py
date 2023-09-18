from python_usrus_bot.database.abstract_repository import AbstractRepository
from python_usrus_bot.models.description import Description


class DescriptionRepository(AbstractRepository):
    async def add(self, user_id: int, description: Description) -> None:
        self.database["description"].insert_one({
            "user_id": user_id,
            "text": description.text})

    async def get(self, user_id: int) -> list[Description]:
        results = await self.database["description"].find({"user_id": user_id}).to_list(None)
        return [Description(0, result["text"]) for result in results]
