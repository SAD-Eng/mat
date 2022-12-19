from __future__ import annotations
from dataclasses import dataclass, field
from . mat_types import BuiltInTypes

@dataclass
class SemVer:
    major : int = 0
    minor : int = 0
    patch : int = 0

@dataclass
class BomVariable:
    name            : str
    description     : str
    var_type        : BuiltInTypes

@dataclass
class BinaryObjectModel:
    name        : str
    description : str = "TBD"
    version     : SemVer = field(default_factory=SemVer)
    variables   : list[BomVariable] = field(default_factory=list)

@dataclass 
class MemoryAtlas:
    mat_version : SemVer = SemVer(0, 1, 0)
    boms        : list[BomVariable] = field(default_factory=list)