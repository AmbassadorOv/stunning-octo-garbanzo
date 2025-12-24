# entities/new_one.py
from dataclasses import dataclass, field
from typing import List, Optional
import uuid

@dataclass
class NewOne:
    glyph: str
    scroll: str
    parent_id: Optional[str] = None
    id: Optional[str] = None
    children: List["NewOne"] = field(default_factory=list)
    compost_log: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.id is None:
            self.id = f"node_{uuid.uuid4().hex[:6].upper()}"

    def breathe(self):
        # In real system: run in thread
        print(f"{self.id} {self.glyph} breathes: {self.scroll}")
        self.compost_log.append(f"[BREATH] {self.scroll}")
