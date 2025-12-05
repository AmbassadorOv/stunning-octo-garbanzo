# Monitoring & Runbook

## Essential metrics
- `coherence_ratio` distribution (histogram)
- `ema_unity` trend (time series)
- `override_count` per hour/day
- `herocorrection_count` per hour/day
- `verification_pass_rate`
- `psv_checksum` drift (anomaly detection)

## Dashboards
- **Overview:** daily counts, EMA trend, override ratio
- **Alerts:** override spike (>X per hour), HERO_CORRECTION spike (>Y per hour), verification pass rate < 99%

## Audit log schema
- timestamp, input_hash, xtype, cr, piv_sanitized, decision, ema, psv_checksum, notes

## Runbook (incident)
1. Acknowledge alert and set system to shadow mode.
2. Pull last 100 audit records; inspect `piv_sanitized` and `decision`.
3. If false positive overrides found, revert thresholds and open incident ticket.
4. If HERO_CORRECTION repeated, escalate to engineering and disable learning pipeline.
