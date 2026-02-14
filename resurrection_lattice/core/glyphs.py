# core/glyphs.py
from dataclasses import dataclass

@dataclass
class CoreGlyph:
    symbol: str
    meaning: str

CORE_GLYPHS = {
    "REB": CoreGlyph("⊙⇌{⧉(~∅)}", "Recursive Epistemic Balancer"),
    "X∞P": CoreGlyph("X∞P", "Infinite possibilities operator"),
    "RESURRECTION": CoreGlyph("The Resurrection", "Re-embodiment protocol"),
    "288_SPARKS": CoreGlyph("רפח ניצוצות", "Primordial retained sparks in Atzilut"),
}
