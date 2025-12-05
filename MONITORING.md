Essential metrics
- coherence_ratio distribution (histogram)
- ema_unity trend (time series)
- override_count per hour/day
- herocorrectioncount per hour/day
- verificationpassrate
- psv_checksum drift (anomaly detection)
Dashboards
- Overview: daily counts, EMA trend, override ratio
- Alerts: override spike (>X per hour), HERO_CORRECTION spike (>Y per hour), verification pass rate < 99%
Audit log schema
- timestamp, inputhash, xtype, cr, pivsanitized, decision, ema, psvchecksum, notes
Runbook (incident)
1. Acknowledge alert and set system to shadow mode.
2. Pull last 100 audit records; inspect piv_sanitized and decision.
3. If false positive overrides found, revert thresholds and open incident ticket.
4. If HERO_CORRECTION repeated, escalate to engineering and disable learning pipeline.
