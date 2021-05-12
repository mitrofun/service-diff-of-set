from datetime import datetime
from enum import IntEnum

import ormar
from ormar import property_field

from src.db import MainMeta


class EnumWithName(IntEnum):
    def __new__(cls, value: int, name: str):
        member = int.__new__(cls, value)
        member._value_ = value
        member._name = name
        return member

    def __int__(self):
        return self._value_

    def __str__(self):
        return self._name

    @classmethod
    def get_choices(cls):
        return [(int(s), str(s)) for s in cls]


class Status(EnumWithName):
    uploaded = 0, 'загружено'
    processed = 1, 'обрабатывается'
    finished = 2, 'обработано'


class Action(EnumWithName):
    not_calculated = 0, 'not calculated'
    added = 1, 'added'
    removed = 2, 'removed'


class Calculation(ormar.Model):
    class Meta(MainMeta):
        tablename = 'calculations'

    id: int = ormar.Integer(primary_key=True)
    file: str = ormar.String(max_length=1000, unique=True)
    status: int = ormar.Integer(choices=list(Status), default=Status.uploaded, index=True)
    action: int = ormar.Integer(default=Action.not_calculated)
    value: int = ormar.Integer(nullable=True)
    create_at: datetime = ormar.DateTime(default=datetime.now)
    finished_at: datetime = ormar.DateTime(nullable=True)

    @property_field
    def display_status(self) -> str:
        return str(Status(self.status))

    @property_field
    def result(self) -> str:
        if self.action == Action.not_calculated:
            return ''
        return f'{Action(self.action)}: {self.value}'

    async def set_processed_status(self) -> None:
        await self.update(status=Status.processed)

    async def set_finished_status(self, value: int, action: str) -> None:
        await self.update(
            action=Action[action],
            value=value,
            status=Status.finished,
            finished_at=datetime.now()
        )
