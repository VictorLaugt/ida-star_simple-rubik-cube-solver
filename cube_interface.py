from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Self

Rotation = TypeVar('Rotation')


class AbstractCube(ABC, Generic[Rotation]):
    # ---- constructors
    @classmethod
    @abstractmethod
    def new_solved(cls) -> Self:
        pass

    @classmethod
    @abstractmethod
    def new_shuffled(cls, n_shuffle: int=1024) -> Self:
        pass

    @abstractmethod
    def copy(self) -> Self:
        pass

    # ---- equality
    def __eq__(self, other: Self) -> bool:
        pass

    # ---- setters
    @abstractmethod
    def shuffle(self, n_shuffle: int=1024) -> list[Rotation]:
        pass

    @abstractmethod
    def apply_rotation(self, rotation: Rotation) -> None:
        pass

    @abstractmethod
    def undo_rotation(self, rotation: Rotation) -> None:
        pass

    @abstractmethod
    def is_solved(self) -> bool:
        pass

    # ---- graphical representation
    @abstractmethod
    def plot(self, ax=None):
        pass
