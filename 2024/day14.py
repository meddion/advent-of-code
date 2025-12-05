import re
import unittest
from dataclasses import dataclass


@dataclass
class XY:
    x: str
    y: str


@dataclass
class Robot:
    pos: XY
    vel: XY


def parse_robot(line: str) -> Robot:
    match = re.search(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line)
    if not match:
        raise ValueError(f"wrong format: {line}")

    return Robot(
        pos=XY(x=int(match.group(1)), y=int(match.group(2))),
        vel=XY(x=int(match.group(3)), y=int(match.group(4))),
    )


def get_safety_factor(robots: str, width: int, height: int) -> int:
    robots = list(map(parse_robot, robots.strip().split("\n")))
    seconds = 100
    w_mid = width // 2
    h_mid = height // 2

    quadrant = [0, 0, 0, 0]
    for robot in robots:
        robot.pos.x = (robot.pos.x + robot.vel.x * seconds) % width
        robot.pos.y = (robot.pos.y + robot.vel.y * seconds) % height

        # First quadrant
        if robot.pos.x < w_mid and robot.pos.y < h_mid:
            quadrant[0] += 1
        elif robot.pos.x > w_mid and robot.pos.y < h_mid:
            quadrant[1] += 1
        elif robot.pos.x < w_mid and robot.pos.y > h_mid:
            quadrant[2] += 1
        elif robot.pos.x > w_mid and robot.pos.y > h_mid:
            quadrant[3] += 1

    return quadrant[0] * quadrant[1] * quadrant[2] * quadrant[3]


class Test(unittest.TestCase):
    def test1_part1(self):
        robots = """
p=2,4 v=2,-3
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=9,5 v=-3,-3
"""
        self.assertEqual(get_safety_factor(robots, 11, 7), 12)


if __name__ == "__main__":
    # unittest.main()
    robots = open("day14.txt", "r").read()
    print(get_safety_factor(robots, 101, 103))
