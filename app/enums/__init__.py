from enum import Enum


class StrEnum(Enum):
    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)

class IntEnum(Enum):
    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        return super().__eq__(other)