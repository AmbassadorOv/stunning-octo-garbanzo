# Staged Rollout & Checklist

Staged rollout: simulation → shadow → limited live (human‑in‑loop) → full autonomy.

## Pre‑deployment (simulation)
- Run pytest and synthetic stress tests (1000 runs) to measure override frequency and HERO_CORRECTION rate.
- Validate deterministic coherence: seed inputs and assert stable outputs.

## Shadow mode
- Deploy service that logs decision and audit_index but does not act.
- Compare suggested actions vs. baseline for 1–2 weeks.

## Limited live (human‑in‑loop)
- Enable EXPLORATION_OVERRIDE_COMMITTED suggestions only after human approval.
- Set alerting for >N overrides/day or repeated HERO_CORRECTION.

## Full autonomy
- Only after verification pass rate > 99.5% and stable EMA trends.

## Rollback & fail‑safe
- Feature flags to disable overrides and force Axiomatic Lock.
- Emergency trigger: if HERO_CORRECTION rate spikes or safety metric breached, auto‑revert to structural lock.
