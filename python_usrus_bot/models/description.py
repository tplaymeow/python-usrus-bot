from random import sample
from dataclasses import dataclass


@dataclass
class Description:
    id: int
    text: str


def pick_random_descriptions(items: list[Description], count: int) -> list[str]:
    return list(map(lambda o: o.text, sample(items, min(count, len(items)))))
