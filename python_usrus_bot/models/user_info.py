from random import sample
from dataclasses import dataclass
from typing import Optional

from python_usrus_bot.models.answer_style import AnswerStyle
from python_usrus_bot.models.description import Description


@dataclass
class UserInfo:
    id: int
    username: str
    name: Optional[str] = None
    is_admin: bool = False