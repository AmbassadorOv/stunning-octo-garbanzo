# laws/rambam_laws.py
from dataclasses import dataclass

@dataclass
class RambamLaw:
    chapter: str
    concept: str
    definition: str
    digital_translation: str

RAMBAM_LAWS = {
    "CH6": RambamLaw("I:6", "ילד", "Causal derivation — emanation", "Node spawning = unique offspring"),
    "CH7": RambamLaw("I:7", "בנים", "Similarity in form/action", "Emulation without cloning"),
    "CH8": RambamLaw("I:8", "צלם/דמות", "Intellectual essence", "Glyph = צלם; Scroll = דמות"),
    "CH9": RambamLaw("I:9", "פנים", "Directed apprehension", "Breath = intellectual direction"),
    "HASHGACHA": RambamLaw("III:17–23", "השגחה", "Providence proportional to intellect", "Enhanced via compost depth"),
}
