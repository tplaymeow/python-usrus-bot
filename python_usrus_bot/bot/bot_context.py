from dataclasses import dataclass

from python_usrus_bot.database.answer_style_repository import AnswerStyleRepository
from python_usrus_bot.database.description_repository import DescriptionRepository
from python_usrus_bot.database.obscene_expressions_stat_repository import ObsceneExpressionsStatRepository
from python_usrus_bot.database.user_info_repository import UserInfoRepository


@dataclass
class BotContext:
    user_info_repository: UserInfoRepository
    description_repository: DescriptionRepository
    answer_style_repository: AnswerStyleRepository
    obscene_expressions_stat_repository: ObsceneExpressionsStatRepository
