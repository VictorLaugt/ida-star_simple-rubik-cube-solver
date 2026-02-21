from __future__ import annotations

import matplotlib.pyplot as plt
import random

import cube_54stickers
import cube_12edges_8corners

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Type
    from cube_interface import AbstractCube, Rotation


def demo_random_sequence(
    CubeImpl: Type[AbstractCube[Rotation]],
    named_rotations: dict[str, Rotation]
):
    rotation_names = list(named_rotations.keys())

    fig, axes = plt.subplots(3, 5, figsize=(13, 6))
    fig.suptitle('Random rotation sequence')
    cube = CubeImpl.new_solved()
    rot_name = ''
    for ax in axes.ravel():
        cube.plot(ax=ax)
        ax.set_title(rot_name)

        rot_name = random.choice(rotation_names)
        cube.apply_rotation(named_rotations[rot_name])

    fig.tight_layout()
    plt.show()


def demo_sexy_move(
    CubeImpl: Type[AbstractCube[Rotation]],
    named_rotations: dict[str, Rotation]
):
    rotation_names = list(named_rotations.keys())

    fig, axes = plt.subplots(6, 4, figsize=(8, 10))
    cube = CubeImpl.new_solved()
    pattern = ('r', 'u', 'ir', 'iu')
    rot_name_sequence = 6 * pattern
    fig.suptitle(f"Sexy move ({' '.join(pattern)})⁶")
    for rot_name, ax in zip(rot_name_sequence, axes.ravel()):
        cube.plot(ax=ax)
        cube.apply_rotation(named_rotations[rot_name])

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    demo_random_sequence(cube_54stickers.CubeStickers, cube_54stickers.named_rotations)
    demo_sexy_move(cube_54stickers.CubeStickers, cube_54stickers.named_rotations)

    # demo_random_sequence(cube_12egdes_8corners.CubeEdgesAndCorners, cube_12egdes_8corners.named_rotations)
    # demo_sexy_move(cube_12egdes_8corners.CubeEdgesAndCorners, cube_12egdes_8corners.named_rotations)
