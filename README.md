# Julius SGL Bundle

## Requirements
- Python 3.9+
- pip

## Install
```bash
pip install -r requirements.txt  # pytest only required for tests
```

## Run demo
```bash
python omnigatesgl.py
```

## Run tests
```bash
pytest -q
```

## Integration notes
- Use `omnigaterun(input, incoming_state, context_config)` as the main API.
- Persist state returned by the function between runs.
- Use `quantic_processor.QuanticProcessor` for the Quantic runtime if you need numeric PSV behavior.

## Deployment
Follow `DEPLOYMENT.md` for staged rollout and `MONITORING.md` for metrics and runbook.
