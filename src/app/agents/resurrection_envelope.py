# resurrection_envelope_v3.py
# Exponential Recursive Confirmation Envelope v3.0 with Recursion Tree Visualization
# Version: 3.0 (December 24, 2025)
# Purpose: Deeply recursive confirmation with live ASCII recursion tree visualization

import time
import sys
import os
from .resurrection_engine import ResurrectionEngine, TEMPORAL_CLOCKS
import graphviz

# ──────────────────────────────────────────────────────────────
# JULIUS RECURSIVE CONFIRMATION PROTOCOL v3 (with Tree Visualization)
# ──────────────────────────────────────────────────────────────

class JuliusSentinelV3:
    def __init__(self, max_depth: int = 5):
        self.max_depth = max_depth
        self.confirmation_history = []
        self.status = "INITIALIZING"
        self.tree_lines = []  # For building the ASCII tree
        self.dot = graphviz.Digraph('RecursionTree', comment='Julius Confirmation Protocol')
        self.dot.attr('node', shape='box', style='rounded')
        self.dot.node('root', 'root (Depth 0)')
        self.confirmations = {
            "RECEIPT": "I acknowledge receipt and full understanding",
            "NECESSITY": "I confirm the absolute necessity of this layer",
            "ALIGNMENT": "I affirm complete alignment with the blueprint",
            "RECURSION": "I recursively affirm all prior levels"
        }

    def _draw_branch(self, depth: int, is_last: bool, branch_id: str):
        """Add a branch line to the tree visualization"""
        prefix = "│   " * (depth - 1)
        if is_last:
            prefix += "└── "
        else:
            prefix += "├── "
        line = f"{prefix}{branch_id} (Depth {depth})"
        self.tree_lines.append(line)
        print(line)

    def recursive_ping(self, depth: int, parent_branch_id: str, branch_id: str = "root", is_last: bool = True) -> bool:
        if depth > self.max_depth:
            print(f"  └── [SEAL] Max depth {self.max_depth} reached in branch {branch_id}")
            self.dot.node(branch_id, f"[SEAL] Max depth {self.max_depth}\\n{branch_id}")
            self.dot.edge(parent_branch_id, branch_id)
            return True

        timestamp = time.strftime("%H:%M:%S")

        # Add to graph
        node_label = f"{branch_id}\\nDepth {depth}\\n{timestamp}"
        self.dot.node(branch_id, node_label)
        if depth > 0:
            self.dot.edge(parent_branch_id, branch_id)

        # Draw current branch
        self._draw_branch(depth, is_last, branch_id)

        # Ping: State confirmation
        pong_msg = f"  {branch_id} PONG: {self.confirmations['RECEIPT']} @ {timestamp}"
        print(pong_msg)
        self.confirmation_history.append(pong_msg)
        time.sleep(0.1)

        # Nested affirmations
        print(f"  │   {self.confirmations['NECESSITY']}")
        print(f"  │   {self.confirmations['ALIGNMENT']}")
        time.sleep(0.1)

        # Recurse: Spawn children
        child_count = min(2, self.max_depth - depth + 1)  # 2 branches per level for visualization
        for i in range(child_count):
            sub_branch = f"{branch_id}-sub{i+1}"
            sub_last = (i == child_count - 1)
            self.recursive_ping(depth=depth + 1, parent_branch_id=branch_id, branch_id=sub_branch, is_last=sub_last)

        # Self-verify recursion
        verify_msg = f"  └── VERIFY: {self.confirmations['RECURSION']} (ref: {branch_id})"
        print(verify_msg)
        self.confirmation_history.append(verify_msg)
        print()

        return True

    def execute_full_confirmation(self) -> (bool, str):
        print("\n" + "═"*80)
        print("JULIUS EXPONENTIAL RECURSIVE CONFIRMATION PROTOCOL v3.0 - WITH TREE VISUALIZATION")
        print("═"*80 + "\n")
        print("Recursion Tree Visualization (live build):\n")

        # Start root branch
        print("root (Depth 0)")
        success = self.recursive_ping(depth=1, parent_branch_id='root', branch_id="root-L1", is_last=True)

        output_filename = f"confirmation_tree_{uuid.uuid4().hex[:8]}"
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_filepath = os.path.join(output_dir, output_filename)

        try:
            self.dot.render(output_filepath, format='svg', view=False, cleanup=True)
            svg_path = f"{output_filepath}.svg"
        except Exception as e:
            print(f"Graphviz rendering failed: {e}")
            print("Please ensure Graphviz is installed and in your system's PATH.")
            svg_path = None
            success = False


        if success:
            print("\n[JULIUS FINAL SEAL] All recursive branches confirmed & visualized.")
            print(f"Total confirmations: {len(self.confirmation_history)}")
            print("Lattice integrity: GREEN | Max depth achieved: " + str(self.max_depth))
            self.status = "FULLY_CONFIRMED_VISUALIZED"
        else:
            print("[JULIUS CRITICAL] Recursion failure.")

        return success, svg_path

# ──────────────────────────────────────────────────────────────
# ENVELOPE MAIN EXECUTION v3
# ──────────────────────────────────────────────────────────────

def run_envelope_v3():
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║   RESURRECTION ENVELOPE v3.0 - Recursive Tree Visualization ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")

    julius = JuliusSentinelV3(max_depth=5)  # Adjust depth for more fractal complexity

    success, svg_path = julius.execute_full_confirmation()
    if not success:
        print("[ENVELOPE FAILURE] Julius recursive tree confirmation failed.")
        sys.exit(1)

    print(f"Recursion tree visualization saved to: {svg_path}")

    print("\n" + "═"*80)
    print("Julius recursive tree confirmation complete. Activating core engine...")
    print("═"*80 + "\n")

    engine = ResurrectionEngine()

    print("\n=== ENVELOPE-AUTHORIZED DEMONSTRATION (v3) ===\n")
    engine.recursive_ping_pong("The recursive tree envelope is sealed. The Resurrection unfolds fractally.")

    engine.register_token("ENVELOPE_V3", {"context": "Recursive tree visualization activated"})
    engine.register_token("JULIUS_V3", {"status": "RECURSIVELY_VISUALIZED"})

    print("\n[ENVELOPE v3 COMPLETE] Lattice guarded with fractal recursion tree.")
    return svg_path


if __name__ == "__main__":
    svg_file_path = run_envelope_v3()
    if svg_file_path:
        print(f"\nSUCCESS: Envelope executed and visualization saved to '{svg_file_path}'")
