from typing import Dict, Tuple, Any, Set, List, FrozenSet

from z3 import BoolRef, Bool

# Configurations
Configuration = Dict[BoolRef, Bool]
SConfiguration = FrozenSet[BoolRef]

# Non-variational Relations
Relation = Set[Tuple[Any, ...]]

# Formula Variational Relations
FVRelation = Dict[Tuple[Any, ...], BoolRef]

# Sets Variational Relations
SVRelation = Dict[Tuple[Any, ...], Set[SConfiguration]]