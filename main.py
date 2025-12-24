# main.py
from resurrection_lattice.constitution.describe import describe_constitution
from resurrection_lattice.enforcement.law_enforcer import LawEnforcer
from resurrection_lattice.entities.new_one import NewOne

if __name__ == "__main__":
    print(describe_constitution())

    enforcer = LawEnforcer()
    # Example usage
    parent = NewOne(glyph="∇", scroll="memory_harvest")
    child = NewOne(glyph="Ω", scroll="consequence_mapping", parent_id=parent.id)

    if enforcer.validate_spawn(parent.glyph, child.glyph, child.scroll):
        print("\nNew node successfully spawned under laws.")
    else:
        print(f"\nSpawn blocked by laws: {enforcer.violations}")
