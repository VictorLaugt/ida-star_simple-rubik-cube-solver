from __future__ import annotations

import matplotlib.pyplot as plt
import random

from cube_54stickers import CubeStickers as Cube
# from cube_12edges_8corners import CubeEdgesAndCorners as Cube

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import TypeVar
    R = TypeVar('R')


def demo_random_sequence() -> None:
    cube = Cube.new_solved()
    possible_rotations = cube.get_possible_rotations()
    rotation_names = list(possible_rotations.keys())

    fig, axes = plt.subplots(3, 5, figsize=(13, 6))
    fig.suptitle('Random rotation sequence')
    rot_name = ''
    for ax in axes.ravel():
        cube.plot(ax=ax)
        ax.set_title(rot_name)

        rot_name = random.choice(rotation_names)
        cube.apply_rotation(possible_rotations[rot_name])

    fig.tight_layout()
    plt.show()


def demo_sexy_move() -> None:
    cube = Cube.new_solved()
    possible_rotations = cube.get_possible_rotations()

    fig, axes = plt.subplots(6, 4, figsize=(8, 10))
    pattern = ('r', 'u', 'ir', 'iu')
    rot_name_sequence = 6 * pattern
    fig.suptitle(f"Sexy move ({' '.join(pattern)})⁶")
    for rot_name, ax in zip(rot_name_sequence, axes.ravel()):
        cube.plot(ax=ax)
        cube.apply_rotation(possible_rotations[rot_name])

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    demo_random_sequence()
    demo_sexy_move()
