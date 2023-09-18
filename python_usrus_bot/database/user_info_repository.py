from typing import Optional

from python_usrus_bot.database.abstract_repository import AbstractRepository
from python_usrus_bot.models.user_info import UserInfo


class UserInfoRepository(AbstractRepository):
    async def add(self, user_info: UserInfo) -> None:
        await self.database["user_info"].insert_one({
            "user_id": user_info.id,
            "username": user_info.username,
            "name": user_info.name,
            "is_admin": user_info.is_admin})

    async def get(self, user_id: int) -> Optional[UserInfo]:
        result = await self.database["user_info"].find_one({"user_id": user_id})
        if result is None:
            return None

        return UserInfo(
            id=result["user_id"],
            username=result["username"],
            name=result["name"],
            is_admin=result.get("is_admin") or False)
