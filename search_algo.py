from __future__ import annotations

from cube_54stickers import (
    CubeStickers as Cube,
    possible_rotations,
    named_rotations
)
# from cube_12edges_8corners import (
    # CubeEdgesAndCorners as Cube,
    # possible_rotations,
    # named_rotations
# )

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Iterator, Callable, Optional
    from cube_interface import AbstractCube, Rotation


def successors(
    node: AbstractCube,
    h: Callable[[AbstractCube], float]
) -> list[tuple[Rotation, AbstractCube, float]]:
    result = []
    for rot in possible_rotations:
        succ = node.copy()
        succ.apply_rotation(rot)
        result.append((rot, succ, h(succ)))

    result.sort(key=lambda x: x[2])
    return result


def _rot_seq_repr(rot_seq: list[Rotation]) -> str:  # FOR DEBUG ONLY
    import numpy as np
    rotation_names = []
    for rot in rot_seq:
        for rot_name, rot_2 in named_rotations.items():
            if np.all(rot == rot_2):
                rotation_names.append(rot_name)
    return ' '.join(rotation_names)


class Path:
    def __init__(self) -> None:
        self.rot_path: list[Optional[Rotation]] = []
        self.node_path: list[AbstractCube] = []

    def __repr__(self) -> str:  # FOR DEBUG ONLY
        return _rot_seq_repr(self.rot_path)

    def __len__(self) ->int:
        return len(self.rot_path)

    def push(self, rot: Opitonal[Rotation], node: AbstractCube) -> None:
        self.rot_path.append(rot)
        self.node_path.append(node)

    def pop(self) -> tuple[Optional[Rotation], AbstractCube]:
        return self.rot_path.pop(), self.node_path.pop()

    def clear(self) -> None:
        self.rot_path.clear()
        self.node_path.clear()

    def contains_node(self, node: AbstractCube) -> bool:
        return node in self.node_path


class IDAStar:
    def __init__(self, h: Callable[[AbstractCube], int]) -> None:
        self.h = h
        self.path = Path()
        self.bound = 0.

    def search(self, root: AbstractCube) -> tuple[Path, Optional[int]]:
        root = root.copy()
        self.bound = self.h(root)
        self.path.clear()
        self.path.push(None, root)

        while True:
            print(f"bound = {self.bound}")
            t = self.dfs(root, 0., self.bound)
            if t == -1.:
                return self.path, self.bound
            if t == float('inf'):
                return self.path, None
            self.bound = t

    def dfs(self, node: AbstractCube, g: float, h: float) -> float:
        f = g + h
        if f > self.bound:
            return f
        if node.is_solved():
            return -1.

        min_t = float('inf')
        for rot, succ, succ_h in successors(node, self.h):
            if self.path.contains_node(succ):
                continue

            self.path.push(rot, succ)

            t = self.dfs(succ, g+1., succ_h)
            if t == -1.:
                return -1.
            if t < min_t:
                min_t = t

            self.path.pop()

        return min_t




if __name__ == '__main__':
    import random
    import numpy as np
    import matplotlib.pyplot as plt

    goal = Cube.new_solved()
    def h(node):
        return np.count_nonzero(node.stickers != goal.stickers) / 20

    # h = lambda node: 0


    cube = Cube.new_solved()

    rand_rot_seq = [random.choice(possible_rotations) for _ in range(7)]
    # rand_rot_seq = [named_rotations[name] for name in ('b b il if ir d il'.split())]
    # rand_rot_seq = [named_rotations[name] for name in ('l id r f l b b'.split())]
    for rot in rand_rot_seq:
        cube.apply_rotation(rot)
    
    print(_rot_seq_repr(rand_rot_seq))
    solver = IDAStar(h)
    path, cost = solver.search(cube)
    print(path)

    cube.plot()
    plt.show()
    for node in path.node_path:
        ax = node.plot()
        plt.show()
