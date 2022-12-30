from enum import IntEnum


class PrimitiveType(IntEnum):
    INT8 = 1
    UINT8 = 2
    INT16 = 3
    UINT16 = 4
    INT32 = 5
    UINT32 = 6
    INT64 = 7
    UINT64 = 8
    INT128 = 9
    UINT128 = 10
    HALF = 11
    SINGLE = 12
    DOUBLE = 13
    QUADRUPLE = 14
    STRING = 15
    BOOLEAN = 16
