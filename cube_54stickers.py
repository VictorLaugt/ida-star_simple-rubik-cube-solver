from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import random

from cube_interface import AbstractCube


rot_b = np.array([
    [36, 38, 44, 42,  39, 37, 41, 43,  29, 0, 15, 53,  32, 1, 12, 52,  35, 2, 9, 51],
    [38, 44, 42, 36,  37, 41, 43, 39,  0, 15, 53, 29,  1, 12, 52, 32,  2, 9, 51, 35]
], dtype=np.int8)

rot_f = np.array([
    [20, 18, 24, 26,  19, 21, 25, 23,  6, 17, 47, 27,  7, 14, 46, 30,  8, 11, 45, 33],
    [18, 24, 26, 20,  21, 25, 23, 19,  17, 47, 27, 6,  14, 46, 30, 7,  11, 45, 33, 8]
], dtype=np.int8)

rot_d = np.array([
    [47, 45, 51, 53,  50, 46, 48, 52,  44, 35, 26, 17,  43, 34, 25, 16,  42, 33, 24, 15],
    [45, 51, 53, 47,  46, 48, 52, 50,  35, 26, 17, 44,  34, 25, 16, 43,  33, 24, 15, 42]
], dtype=np.int8)

rot_u = np.array([
    [3, 1, 5, 7,  0, 2, 8, 6,  38, 29, 20, 11,  37, 28, 19, 10,  36, 27, 18, 9],
    [1, 5, 7, 3,  2, 8, 6, 0,  29, 20, 11, 38,  28, 19, 10, 37,  27, 18, 9, 36]
], dtype=np.int8)

rot_l = np.array([
    [12, 10, 14, 16,  9, 11, 17, 15,  0, 18, 45, 44,  3, 21, 48, 41,  6, 24, 51, 38],
    [10, 14, 16, 12,  11, 17, 15, 9,  18, 45, 44, 0,  21, 48, 41, 3,  24, 51, 38, 6]
], dtype=np.int8)

rot_r = np.array([
    [32, 28, 30, 34,  29, 27, 33, 35,  2, 20, 47, 42,  5, 23, 50, 39,  8, 26, 53, 36],
    [28, 30, 34, 32,  27, 33, 35, 29,  20, 47, 42, 2,  23, 50, 39, 5,  26, 53, 36, 8]
], dtype=np.int8)

rot_ib = rot_b[[1, 0]]
rot_if = rot_f[[1, 0]]
rot_id = rot_d[[1, 0]]
rot_iu = rot_u[[1, 0]]
rot_il = rot_l[[1, 0]]
rot_ir = rot_r[[1, 0]]

possible_rotations = (
    rot_b, rot_f, rot_d, rot_u, rot_l, rot_r,
    rot_ib, rot_if, rot_id, rot_iu, rot_il, rot_ir
)

named_rotations = {
    'b': rot_b, 'f': rot_f, 'd': rot_d, 'u': rot_u, 'l': rot_l, 'r': rot_r,
    'ib': rot_ib, 'if': rot_if, 'id': rot_id, 'iu': rot_iu, 'il': rot_il, 'ir': rot_ir
}


class CubeStickers(AbstractCube[np.ndarray]):
    solved_stickers = np.zeros(54, dtype=np.int8)
    solved_stickers[0:9] = 0    # U
    solved_stickers[9:18] = 1   # L
    solved_stickers[18:27] = 2  # F
    solved_stickers[27:36] = 3  # R
    solved_stickers[36:45] = 4  # B
    solved_stickers[45:54] = 5  # D

    def __init__(self, stickers: np.ndarray) -> None:
        self.stickers = stickers

    def _color_array_2d(self) -> np.ndarray:
        plan = np.full((9, 12), -1, dtype=np.int8)
        plan[0:3, 3:6] = self.stickers[0:9].reshape(3, 3)     # U
        plan[3:6, 0:3] = self.stickers[9:18].reshape(3, 3)    # L
        plan[3:6, 3:6] = self.stickers[18:27].reshape(3, 3)   # F
        plan[3:6, 6:9] = self.stickers[27:36].reshape(3, 3)   # R
        plan[3:6, 9:12] = self.stickers[36:45].reshape(3, 3)  # B
        plan[6:9, 3:6] = self.stickers[45:54].reshape(3, 3)   # D
        return plan        

    def __str__(self) -> str:
        str_builder = []
        for row in self._color_array_2d():
            colors = ''.join((f' {color} ' if color > -1 else '   ') for color in row)
            str_builder.append(colors)
        return '\n'.join(str_builder) + '\n'


    @classmethod
    def new_solved(cls) -> CubeStickers:
        return cls(cls.solved_stickers.copy())

    @classmethod
    def new_shuffled(cls, n_shuffle: int=1024) -> CubeStickers:
        cube = cls(cls.solved_stickers.copy())
        cube.shuffle(n_shuffle)
        return cube

    def __eq__(self, other: CubeStickers) -> bool:
        return np.all(self.stickers == other.stickers)

    def copy(self) -> CubeStickers:
        return CubeStickers(self.stickers.copy())

    def shuffle(self, n_shuffle: int=1024) -> list[np.ndarray]:
        random_rot_sequence = []
        for _ in range(n_shuffle):
            random_rot = random.choice(possible_rotations)
            random_rot_sequence.append(random_rot)
            self.apply_rotation(random_rot)
        return random_rot_sequence

    def apply_rotation(self, rotation: np.ndarray) -> None:
        src_idx, dst_idx = rotation[0, :], rotation[1, :]
        self.stickers[dst_idx] = self.stickers[src_idx]

    def undo_rotation(self, rotation: np.ndarray) -> None:
        src_idx, dst_idx = rotation[0, :], rotation[1, :]
        self.stickers[src_idx] = self.stickers[dst_idx]

    def is_solved(self) -> bool:
        return np.all(self.stickers == self.solved_stickers)

    def plot(self, ax=None):
        if ax is None:
            _, ax = plt.subplots()

        im = ax.imshow(
            self._color_array_2d(),
            cmap=ListedColormap(('black', 'grey', 'orange', 'green', 'red', 'blue', 'yellow'))
        )
        ax.axis('off')
        return ax, im


if __name__ == '__main__':
    cube = CubeStickers.new_solved()

    name_sequence = '''
    r b f r u f if
    iu ir ib if ir
    '''.split()

    cube.plot()
    plt.show()
    for rot_name in name_sequence:
        cube.apply_rotation(named_rotations[rot_name])
        cube.plot()
        plt.show()
