from abc import ABC, abstractmethod
import pickle  # noqa: S403
from typing import Any

import orjson


__all__ = [
    "AbstractSerializer",
    "JSONSerializer",
    "PickleSerializer",
]


class AbstractSerializer(ABC):
    @abstractmethod
    def serialize(self, obj: Any) -> bytes:
        """Сериализует объект в бинарный формат"""

    @abstractmethod
    def deserialize(self, obj: bytes) -> Any:
        """Восстанавливает объект из бинарных данных"""


class JSONSerializer(AbstractSerializer):
    def serialize(self, obj: Any) -> bytes:  # noqa: PLR6301
        return orjson.dumps(obj)

    def deserialize(self, obj: bytes) -> Any:  # noqa: PLR6301
        return orjson.loads(obj)


class PickleSerializer(AbstractSerializer):
    def serialize(self, obj: Any) -> bytes:  # noqa: PLR6301
        return pickle.dumps(obj)

    def deserialize(self, obj: bytes) -> Any:  # noqa: PLR6301
        return pickle.loads(obj)  # noqa: S301
