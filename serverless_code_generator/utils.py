import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Column:
    name: str
    type: str
    nullable: bool

@dataclass
class Table:
    name: str
    columns: List[Column] = field(default_factory=list)
    primary_key: Optional[str] = None

@dataclass
class MetaModel:
    tables: List[Table]
