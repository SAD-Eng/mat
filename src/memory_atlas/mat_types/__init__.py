from typing import Union
from . primitive import PrimitiveType
from . complex import Range, AInt, UAInt, SFixed, UFixed

BuiltInTypes = Union[PrimitiveType, Range, AInt, UAInt, SFixed, UFixed]