from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class SemVer:
  major : int = 0
  minor : int = 0
  patch : int = 0

@dataclass 
class MemoryAtlas:
  def __init__(self):
    self.boms = []  # list of BinaryObjectModel

@dataclass
class BomVariable:
    name : str
    description : str = "TBD"

@dataclass
class BinaryObjectModel:
    name : str
    description : str = "TBD"
    version : SemVer = field(default_factory=SemVer)
    variables : list[BomVariable] = field(default_factory=list)
