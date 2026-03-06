from __future__ import annotations

from cube_54stickers import CubeStickers as Cube
# from cube_12edges_8corners import CubeEdgesAndCorners as Cube

import time

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable, Optional
    from cube_interface import AbstractCube

from typing import Generic, TypeVar
R = TypeVar('R')


class Path:
    def __init__(self) -> None:
        self.rot_name_path: list[Optional[str]] = []
        self.node_path: list[AbstractCube] = []

    def __repr__(self) -> str:
        return ' '.join((rot_name or '_') for rot_name in self.rot_name_path)

    def __len__(self) -> int:
        return len(self.rot_path)

    def push(self, rotation_name: Optional[str], node: AbstractCube) -> None:
        self.rot_name_path.append(rotation_name)
        self.node_path.append(node)

    def pop(self) -> tuple[Optional[str], AbstractCube]:
        return (
            self.rot_name_path.pop(),
            self.node_path.pop()
        )

    def clear(self) -> None:
        self.rot_name_path.clear()
        self.node_path.clear()

    def contains_node(self, node: AbstractCube) -> bool:
        return node in self.node_path


class IDAStar(Generic[R]):
    def __init__(self, h: Callable[[AbstractCube[R]], float]) -> None:
        self.h = h
        self.path = Path()
        self.bound = 0.

    def search(self, root: AbstractCube) -> tuple[Path, Optional[float]]:
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
        for name, succ, succ_h in self.successors(node, self.h):
            if self.path.contains_node(succ):
                continue

            self.path.push(name, succ)

            t = self.dfs(succ, g+1., succ_h)
            if t == -1.:
                return -1.
            if t < min_t:
                min_t = t

            self.path.pop()

        return min_t

    def successors(
        self,
        node: AbstractCube[R],
        h: Callable[[AbstractCube[R]], float]
    ) -> list[tuple[str, AbstractCube[R], float]]:
        result = []
        for rot_name, rot in node.get_possible_rotations().items():
            succ = node.copy()
            succ.apply_rotation(rot)
            result.append((rot_name, succ, h(succ)))

        result.sort(key=lambda x: x[2])
        return result


class IDAStarPerfCount(IDAStar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expansion_count = 0

    def successors(self, *args, **kwargs):
        result = super().successors(*args, **kwargs)
        self.expansion_count += len(result)
        return result

    def search(self, *args, **kwargs):
        start_time = time.perf_counter()
        result = super().search(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Expanded {self.expansion_count} nodes in {end_time - start_time:.2f}s")
        return result


if __name__ == '__main__':
    import random
    import numpy as np
    import matplotlib.pyplot as plt

    goal = Cube.new_solved()
    def h(node):
        return np.count_nonzero(node.stickers != goal.stickers) / 20

    # h = lambda node: 0

    cube = Cube.new_solved()

    rot_name_seq, rot_seq = cube.shuffle(7)
    # rot_name_seq = 'b b il if ir d il'.split()
    # rot_name_seq = 'l id r f l b b'.split()
    # rot_name_seq = 'id u if f l l ib'.split()
    possible_rotations = cube.get_possible_rotations()
    rot_seq = [possible_rotations[rot_name] for rot_name in rot_name_seq]
    for rot in rot_seq:
        cube.apply_rotation(rot)

    print(' '.join(rot_name_seq))
    solver = IDAStarPerfCount(h)
    path, cost = solver.search(cube)
    print(path)

    cube.plot()
    plt.show()
    for node in path.node_path:
        ax = node.plot()
        plt.show()
