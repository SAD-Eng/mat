from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union
from enum import IntEnum
from . mat_types import BuiltInTypes, Range

class ArrayBoundType(IntEnum):
    FIXED = 0 
    VARIABLE = 1

@dataclass
class SemVer:
    major : int = 0
    minor : int = 0
    patch : int = 0

@dataclass
class BomVariable:
    name                : str
    description         : str
    #How do we want to reference a BOM model?
    var_type            : Union[BuiltInTypes, str] 
    array               : bool = False
    array_bound_type    : ArrayBoundType = field(default_factory=lambda: ArrayBoundType.FIXED)
    var_array_bound     : Union[string, None] = None
    var_array_fixed     : Union[string, None] = None
    spare               : boolean = False
    reserved            : boolean = False
    range_constraint    : Union[Range, None] = None

    def validate(self):
        """TODO: Validate the BOM variable is valid."""
        pass

@dataclass
class BinaryObjectModel:
    name        : str
    description : str = "TBD"
    version     : SemVer = field(default_factory=SemVer(1, 0, 0))
    variables   : list[BomVariable] = field(default_factory=list)

@dataclass 
class MemoryAtlas:
    mat_version : SemVer = field(default_factory=lambda : SemVer(0, 1, 0))
    boms        : list[BomVariable] = field(default_factory=list)
