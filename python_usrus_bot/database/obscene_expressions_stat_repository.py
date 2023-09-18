import datetime
from typing import Optional

from python_usrus_bot.database.abstract_repository import AbstractRepository
from python_usrus_bot.models.obscene_expressions_stat import ObsceneExpressionsStat


class ObsceneExpressionsStatRepository(AbstractRepository):
    async def add_or_update(self, user_id: int, stat: ObsceneExpressionsStat) -> None:
        await self.database["obscene_expressions_stat"].update_one(
            filter={"user_id": user_id},
            update={
                "$set": {
                    "user_id": user_id, "date": stat.date.isoformat(), "count": stat.count}},
            upsert=True)

    async def get(self, user_id: int) -> Optional[ObsceneExpressionsStat]:
        result = await self.database["obscene_expressions_stat"].find_one({"user_id": user_id})
        if result is None:
            return None

        return ObsceneExpressionsStat(
            date=datetime.date.fromisoformat(result["date"]),
            count=result["count"])
