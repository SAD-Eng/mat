from dataclasses import dataclass


@dataclass
class Range:
    low   : int
    high  : int

    def __post_init__(self):
        assert self.high >= self.low, f"Range high constraint must be greater than or equal to it's low constraint."


@dataclass
class AInt:
    size : int


@dataclass
class UAInt:
    size : int


@dataclass
class SFixed:
    int_bits  : int
    frac_bits : int


@dataclass
class UFixed:
    int_bits  : int
    frac_bits : int
