from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union
from enum import IntEnum, IntFlag, auto

from . mat_types import BuiltInTypes, Range


class ArrayBoundType(IntEnum):
    FIXED = auto()
    VARIABLE = auto()


class AccessType(IntFlag):
    READ = auto()
    WRITE = auto()


class ReadWriteAction(IntEnum):
    NO_ACTION = auto()
    CLEAR = auto()  # value is 0 after read/write
    SET = auto()  # value is all bits set after read/write
    MODIFY = auto()  # value is modified in some special way after read/write, see description


class Endianness(IntEnum):
    LITTLE = auto()
    BIG = auto()


@dataclass
class SemVer:
    major : int = 0
    minor : int = 0
    patch : int = 0

    def __str__(self):
        return f'{self.major}.{self.minor}.{self.patch}'


@dataclass
class BomVariable:
    """
    A variable within a parent Binary Object Model (BOM).
    """
    name                : str
    description         : str
    var_type            : Union[BuiltInTypes, str]  # when str, is a BinaryObjectModel.name
    array               : bool = False
    array_bound_type    : ArrayBoundType = field(default_factory=lambda: ArrayBoundType.FIXED)
    var_array_bound     : Union[str, None] = None
    var_array_fixed     : Union[str, None] = None
    spare               : bool = False
    reserved            : bool = False
    range_constraint    : Union[Range, None] = None

    def validate(self):
        """TODO: Validate the BOM variable is valid."""
        print('TODO')


@dataclass
class BinaryObjectModel:
    """
    A Binary Object Model (BOM) describes structured binary data. This is an abstract data model that does not
    contain implementation specifics such as an address (memory mapped) or offset (streamed). A BOM can be used
    in a variety of situations such as a variable type in another BOM, the definition of memory-mapped registers,
    an item in a memory-mapped FIFO, or the data of a streamed packet.
    """
    name        : str
    description : str = "TBD"
    version     : SemVer = field(default_factory=SemVer(1, 0, 0))
    variables   : list[BomVariable] = field(default_factory=list)


@dataclass
class MemoryRegion:
    """A memory region is an address range assigned to a top level BOM of a memory map."""
    bom            : str  # BinaryObjectModel.name
    address_offset : int
    size           : int


@dataclass
class Register(MemoryRegion):
    """
    A register memory region indicates the entire BOM mapped to a series of physical registers.
    Each register is addressable. Eventually each variable in a BOM will decompose into a built-in type.
    For each variable, a number of attributes must be defined.
    """
    software_access : AccessType
    hardware_access : AccessType
    reset_mask      : bool
    reset_value     : Union[BuiltInTypes] = None
    read_action     : ReadWriteAction = ReadWriteAction.NO_ACTION
    write_action    : ReadWriteAction = ReadWriteAction.NO_ACTION


@dataclass
class MemoryMap:
    """
    A memory map is intended to be overlaid onto one more BOM. That is the memory map does not define any data.
    The memory map defines behavior and attributes when that data is viewed through a memory mapped architecture.
    """
    name        : str
    description : str = "TBD"
    endianness  : Endianness = Endianness.LITTLE
    regions     : list[MemoryRegion] = field(default_factory=list)


@dataclass 
class MemoryAtlas:
    mat_version : SemVer = field(default_factory=lambda : SemVer(0, 1, 0))
    boms        : list[BinaryObjectModel] = field(default_factory=list)
