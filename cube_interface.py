from __future__ import annotations

import random

from abc import ABC, abstractmethod
from typing import Sequence, TypeVar, Generic, Self

Rotation = TypeVar('Rotation')


class AbstractCube(ABC, Generic[Rotation]):
    # ---- constructors
    @classmethod
    @abstractmethod
    def new_solved(cls) -> Self:
        pass

    @classmethod
    def new_shuffled(cls, n_shuffle: int=1024) -> Self:
        cube = cls.new_solved()
        cube.shuffle(n_shuffle)
        return cube

    @classmethod
    def new(cls, rotation_name_seq: Sequence[str]) -> Self:
        cube = cls.new_solved()
        possible_rotations = cube.get_possible_rotations()
        for rot_name in rotation_name_seq:
            cube.apply_rotation(possible_rotations[rot_name])
        return cube

    @abstractmethod
    def copy(self) -> Self:
        pass

    # ---- rotations
    def get_possible_rotations(self) -> dict[str, Rotation]:
        pass

    # ---- equality
    def __eq__(self, other: Self) -> bool:
        pass

    # ---- setters
    def shuffle(self, n_shuffle: int=1024) -> tuple[list[str], list[Rotation]]:
        possible_rotations = list(self.get_possible_rotations().items())
        rotation_name_seq = []
        rotation_seq = []
        for _ in range(n_shuffle):
            rot_name, rot = random.choice(possible_rotations)
            rotation_name_seq.append(rot_name)
            rotation_seq.append(rot)
            self.apply_rotation(rot)
        return rotation_name_seq, rotation_seq

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
