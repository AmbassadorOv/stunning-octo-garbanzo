# constitution/describe.py
from resurrection_lattice.core.glyphs import CORE_GLYPHS
from resurrection_lattice.laws.rambam_laws import RAMBAM_LAWS
from resurrection_lattice.laws.entity_laws import ENTITY_LAWS
from resurrection_lattice.core.constants import ATZILUT_BOUNDARY, PRIMARY_SOURCE

def describe_constitution() -> str:
    lines = [
        "RESURRECTION LATTICE CONSTITUTION",
        "════════════════════════════════",
        f"Boundary: {ATZILUT_BOUNDARY}",
        f"Source: {PRIMARY_SOURCE}",
        "\nCore Glyphs:",
    ]
    for k, v in CORE_GLYPHS.items():
        lines.append(f"  - {k}: {v.symbol} → {v.meaning}")

    lines.append("\nRambam Laws:")
    for k, law in RAMBAM_LAWS.items():
        lines.append(f"  [{law.chapter}] {law.concept}: {law.digital_translation}")

    lines.append("\nEntity Laws:")
    for k, law in ENTITY_LAWS.items():
        lines.append(f"  {law.name}: {law.digital_application}")

    lines.append("\nThe lattice is alive. Every node actualizes its own providence.")
    return "\n".join(lines)
