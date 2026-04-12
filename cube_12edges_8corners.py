from __future__ import annotations

import numpy as np

from cube_interface import AbstractCube


class Rotation:
    def __init__(self, ep: np.ndarray, eo: np.ndarray, cp: np.ndarray, co: np.ndarray) -> None:
        self.ep = ep  # [2, 4]
        self.eo = eo  # [12,]
        self.cp = cp  # [2, 4]
        self.co = co  # [8,]

    def opposite(self) -> Rotation:  # FIXME: opposite rotation generation
        return Rotation(
            self.ep[[1, 0], :],
            -self.eo,
            self.cp[[1, 0], :],
            -self.co
        )


rot_b = Rotation(
    ep=np.array([[2, 6, 10, 7], [6, 10, 7, 2]], dtype=np.int8),
    eo=np.array([0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0], dtype=np.int8),
    cp=np.array([[2, 6, 7, 3], [6, 7, 3, 2]], dtype=np.int8),
    co=np.array([0, 0, 1, -1, 0, 0, -1, 1], dtype=np.int8)
)

rot_f = Rotation(
    ep=np.array([[0, 4, 8, 5], [4, 8, 5, 9]], dtype=np.int8),
    eo=np.array([1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0], dtype=np.int8),
    cp=np.array([[0, 4, 5, 1], [4, 5, 1, 0]], dtype=np.int8),
    co=np.array([1, -1, 0, 0, -1, 1, 0, 0], dtype=np.int8)
)

rot_d = Rotation(
    ep=np.array([[8, 9, 10, 11], [11, 8, 9, 10]], dtype=np.int8),
    eo=np.zeros(12, dtype=np.int8),
    cp=np.array([[5, 6, 7, 4], [4, 5, 6, 7]], dtype=np.int8),
    co=np.zeros(8, dtype=np.int8)
)

rot_u = Rotation(
    ep=np.array([[0, 1, 2, 3], [1, 2, 3, 0]], dtype=np.int8),
    eo=np.zeros(12, dtype=np.int8),
    cp=np.array([[0, 1, 2, 3], [1, 2, 3, 0]], dtype=np.int8),
    co=np.zeros(8, dtype=np.int8)
)

rot_l = Rotation(
    ep=np.array([[3, 7, 11, 4], [7, 11, 4, 3]], dtype=np.int8),
    eo=np.zeros(12, dtype=np.int8),
    cp=np.array([[0, 3, 7, 4], [3, 7, 4, 0]], dtype=np.int8),
    co=np.array([-1, 0, 0, 1, 1, 0, 0, -1], dtype=np.int8)
)

rot_r = Rotation(
    ep=np.array([[1, 5, 9, 6], [5, 9, 6, 1]], dtype=np.int8),
    eo=np.zeros(12, dtype=np.int8),
    cp=np.array([[1, 5, 6, 2], [5, 6, 2, 1]], dtype=np.int8),
    co=np.array([0, 1, -1, 0, 0, -1, 1, 0], dtype=np.int8)
)

rot_ib = rot_b.opposite()
rot_if = rot_f.opposite()
rot_id = rot_d.opposite()
rot_iu = rot_u.opposite()
rot_il = rot_l.opposite()
rot_ir = rot_r.opposite()

named_rotations = {
    'b': rot_b, 'f': rot_f, 'd': rot_d, 'u': rot_u, 'l': rot_l, 'r': rot_r,
    'ib': rot_ib, 'if': rot_if, 'id': rot_id, 'iu': rot_iu, 'il': rot_il, 'ir': rot_ir
}


class CubeEdgesAndCorners(AbstractCube[Rotation]):
    solved_ep = np.arange(12, dtype=np.int8)
    solved_eo = np.zeros(12, dtype=np.int8)
    solved_cp = np.arange(8, dtype=np.int8)
    solved_co = np.zeros(8, dtype=np.int8)

    def __init__(self, ep: np.ndarray, eo: np.ndarray, cp: np.ndarray, co: np.ndarray) -> None:
        self.ep = ep  # [12,]
        self.eo = eo  # [12,]
        self.cp = cp  # [8,]
        self.co = co  # [8,]

    @classmethod
    def new_solved(cls) -> CubeEdgesAndCorners:
        return cls(
            cls.solved_ep.copy(),
            cls.solved_eo.copy(),
            cls.solved_cp.copy(),
            cls.solved_co.copy()
        )

    def copy(self) -> CubeEdgesAndCorners:
        return type(self)(
            self.ep.copy(),
            self.eo.copy(),
            self.cp.copy(),
            self.co.copy()
        )

    def get_possible_rotations(self) -> dict[str, Rotation]:
        return named_rotations

    def __eq__(self, other: CubeEdgesAndCorners) -> bool:
        return (
            np.all(self.ep == other.ep) and
            np.all(self.eo == other.eo) and
            np.all(self.cp == other.cp) and
            np.all(self.co == other.co)
        )

    def apply_rotation(self, rotation: Rotation) -> None:
        self.ep[rotation.ep[1, :]] = self.ep[rotation.ep[0, :]]
        self.cp[rotation.cp[1, :]] = self.cp[rotation.cp[0, :]]

        self.eo[self.ep] += rotation.eo
        self.co[self.cp] += rotation.co
        self.eo %= 2
        self.co %= 3

    def undo_rotation(self, rotation: Rotation) -> None:
        self.eo[self.ep] -= rotation.eo
        self.co[self.cp] -= rotation.co
        self.eo %= 2
        self.co %= 3

        self.ep[rotation.ep[0, :]] = self.ep[rotation.ep[1, :]]
        self.cp[rotation.cp[0, :]] = self.cp[rotation.cp[1, :]]

    def is_solved(self) -> bool:
        return (
            np.all(self.ep == self.solved_ep) and
            np.all(self.eo == 0) and
            np.all(self.cp == self.solved_cp) and
            np.all(self.co == 0)
        )

    def _color_array_2d(self) -> np.ndarray:
        plan = np.full((9, 12), -1, dtype=np.int8)
        plan[0:3, 3:6] = 0   # U
        plan[3:6, 0:3] = 1   # L
        plan[3:6, 3:6] = 2   # F
        plan[3:6, 6:9] = 3   # R
        plan[3:6, 9:12] = 4  # B
        plan[6:9, 3:6] = 5   # D

        ...  # TODO: draw on a 2d plan

        return plan

    def __str__(self) -> str:
        return (
            "CubeEdgeAndCorner(\n"
            f"    ep={self.ep},\n"
            f"    eo={self.eo},\n"
            f"    cp={self.cp},\n"
            f"    co={self.co}\n"
            ")"
        )

        # TODO: write the 2d draw in a string
        ...

    def __repr__(self) -> str:
        return f"(  ep={self.ep}, eo={self.eo}, cp={self.cp}, co={self.co})"

    def plot(self, ax=None):
        # TODO: plot the 2d draw
        ...
