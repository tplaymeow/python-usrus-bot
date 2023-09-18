from python_usrus_bot.database.abstract_repository import AbstractRepository
from python_usrus_bot.models.answer_style import AnswerStyle


class AnswerStyleRepository(AbstractRepository):
    async def add(self, user_id: int, style: AnswerStyle) -> None:
        await self.database["answer_style"].insert_one({
            "user_id": user_id,
            "text": style.text})

    async def get(self, user_id: int) -> list[AnswerStyle]:
        results = await self.database["answer_style"].find({"user_id": user_id}).to_list(None)
        return [AnswerStyle(0, result["text"]) for result in results]
