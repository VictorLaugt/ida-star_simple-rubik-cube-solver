from __future__ import annotations

import unittest
from itertools import product
import random

import cube_54stickers
import cube_12edges_8corners

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Type
    from cube_interface import AbstractCube, Rotation


def opposite_rotation_name(rot_name: str) -> str:
    if rot_name.startswith('i'):
        return rot_name[1:]
    else:
        return f'i{rot_name}'


def factory_test_rotation_cycle(
    CubeImpl: Type[AbstractCube[Rotation]],
    rot: Rotation
):
    def test_rotation_cycle(self):
        cube = CubeImpl.new_shuffled()
        cube_copy = cube.copy()
        for _ in range(4):
            cube.apply_rotation(rot)
        self.assertEqual(cube, cube_copy)
    return test_rotation_cycle


def factory_test_opposite_rotations(
    CubeImpl: Type[AbstractCube[Rotation]],
    rot: Rotation,
    opp: Rotation
):
    def test_opposite_rotations(self):
        cube = CubeImpl.new_shuffled()
        cube_copy = cube.copy()
        cube.apply_rotation(rot)
        cube.apply_rotation(opp)
        self.assertEqual(cube, cube_copy)
    return test_opposite_rotations


def factory_test_undo_rotation(
    CubeImpl: Type[AbstractCube[Rotation]],
    rot: Rotation,
    opp: Rotation
):
    def test_undo_rotation(self):
        cube = CubeImpl.new_shuffled()
        cube_copy = cube.copy()
        cube.undo_rotation(rot)
        cube_copy.apply_rotation(opp)
        self.assertEqual(cube, cube_copy)
    return test_undo_rotation


def factory_test_sequence_identity(
    CubeImpl: Type[AbstractCube[Rotation]],
    named_rotations: dict[str, Rotation],
    rot_name1: str,
    rot_name2: str
):
    opp_name1 = opposite_rotation_name(rot_name1)
    opp_name2 = opposite_rotation_name(rot_name2)
    rot1, rot2 = named_rotations[rot_name1], named_rotations[rot_name2]
    opp1, opp2 = named_rotations[opp_name1], named_rotations[opp_name2]
    pattern_name = f'{rot_name1}{rot_name2}{opp_name1}{opp_name2}'
    sequence = 6 * (rot1, rot2, opp1, opp2)

    def test_sequence_identity(self):
        cube = CubeImpl.new_solved()
        for rot in sequence[:-1]:
            cube.apply_rotation(rot)
            self.assertFalse(cube.is_solved())

        cube.apply_rotation(sequence[-1])
        self.assertTrue(cube.is_solved())

    return test_sequence_identity, pattern_name


def factory_TestCubeImpl(
    CubeImpl: Type[AbstractCube[Rotation]],
    named_rotations: dict[str, Rotation]
) -> Type[unittest.TestCase]:

    rotation_names = list(named_rotations.keys())
    random_rot_name = (lambda: random.choice(rotation_names))

    class TestCubeImpl(unittest.TestCase):
        def test_init(self):
            cube = CubeImpl.new_solved()
            self.assertTrue(cube.is_solved())

            cube.apply_rotation(named_rotations[random_rot_name()])
            self.assertFalse(cube.is_solved())

        def test_copy(self):
            cube = CubeImpl.new_shuffled()
            cube_copy = cube.copy()
            self.assertEqual(cube, cube_copy)

            cube.apply_rotation(named_rotations[random_rot_name()])
            self.assertNotEqual(cube, cube_copy)

    for rot_name in rotation_names:
        opp_name = opposite_rotation_name(rot_name)
        rot = named_rotations[rot_name]
        opp = named_rotations[opp_name]

        test_rot_cycle = factory_test_rotation_cycle(CubeImpl, rot)
        setattr(TestCubeImpl, f'test_cycle_{rot_name}', test_rot_cycle)

        test_opp_rot = factory_test_opposite_rotations(CubeImpl, rot, opp)
        setattr(TestCubeImpl, f'test_rotation_{rot_name}_{opp_name}', test_opp_rot)

        test_undo = factory_test_undo_rotation(CubeImpl, rot, opp)
        setattr(TestCubeImpl, f'test_undo_{rot_name}', test_undo)

    opposite_faces = {'ud', 'du', 'lr', 'rl', 'fb', 'bf'}
    for rot_name1, rot_name2 in product('bfdulr', 'bfdulr'):
        if rot_name1 == rot_name2 or f'{rot_name1}{rot_name2}' in opposite_faces:
            continue

        test_seq_identity, pattern_name = factory_test_sequence_identity(
            CubeImpl, named_rotations, rot_name1, rot_name2
        )
        setattr(TestCubeImpl, f'test_identity_{pattern_name}_6', test_seq_identity)

    TestCubeImpl.__name__ = TestCubeImpl.__qualname__ = f'Test{CubeImpl.__name__}'
    return TestCubeImpl


TestCubeStickers = factory_TestCubeImpl(
    cube_54stickers.CubeStickers, cube_54stickers.named_rotations
)

TestCubeEdgesAndCorners = factory_TestCubeImpl(
    cube_12edges_8corners.CubeEdgesAndCorners, cube_12edges_8corners.named_rotations
)


if __name__ == '__main__':
    unittest.main(verbosity=2)
