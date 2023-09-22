import datetime
from dataclasses import dataclass


@dataclass
class ObsceneExpressionsStat:
    date: datetime.date
    count: int

    @property
    def is_outdated(self) -> bool:
        return self.date != datetime.date.today()
