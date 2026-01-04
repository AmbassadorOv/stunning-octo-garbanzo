import time
from typing import Dict, Any

class ExecutionObserver:
    """
    Observes the sequential, time-bound execution of the 'thread of R&M'
    against the ideal, non-temporal design. Tracks Quality Adherence (ΔQ).
    """
    def __init__(self, design_id: str):
        self.design_id: str = design_id
        self.start_time: float = time.time()
        self.sequential_stages: Dict[str, Dict[str, Any]] = {}
        self.quality_adherence_factor: float = 1.0 # Start at perfect quality

    def record_stage_start(self, stage_name: str) -> None:
        """Records the initiation of a new step in the descending thread."""
        self.sequential_stages[stage_name] = {
            "start_ts": time.time(),
            "status": "IN_PROGRESS"
        }

    def record_stage_finish(self, stage_name: str, quality_check_result: bool) -> None:
        """Records the completion of a step and its adherence (LUQG check)."""
        if stage_name in self.sequential_stages and self.sequential_stages[stage_name]["status"] == "IN_PROGRESS":
            duration = time.time() - self.sequential_stages[stage_name]["start_ts"]

            self.sequential_stages[stage_name].update({
                "duration": duration,
                "status": "COMPLETED",
                "quality_delta_check": quality_check_result
            })
            if not quality_check_result:
                 # Penalty for deviating from the Intellectual Blueprint
                self.quality_adherence_factor *= 0.95

    def finalize_execution(self) -> float:
        """Marks the end of the R&M line and returns the final adherence metric."""
        total_duration = time.time() - self.start_time

        print("\n--- EXECUTION REALITY REPORT (The Descent) ---")
        print(f"Total Time (Reality Constraint): {total_duration:.4f} seconds")
        print(f"Final Quality Adherence (Preservation of Design): {self.quality_adherence_factor * 100:.2f}%")
        print("---------------------------------------------")
        return self.quality_adherence_factor
