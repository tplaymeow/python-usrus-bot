from dataclasses import dataclass
from random import sample


@dataclass
class AnswerStyle:
    id: int
    text: str


def pick_random_styles(items: list[AnswerStyle], count: int) -> list[str]:
    return list(map(lambda o: o.text, sample(items, min(count, len(items)))))
