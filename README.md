# Julius SGL Bundle

## Requirements
- Python 3.9+
- pip
- numpy

## Install
```bash
pip install -r requirements.txt
```

## Run demo
```bash
python omnigatesgl.py
```

## Run tests
```bash
PYTHONPATH=. pytest -q
```

## Integration notes
- Use `OmniGateSGL(code, state).run()` as the main API.
- The `run()` method returns a dictionary with the following structure:
  ```json
  {
      "final_fidelity": float,
      "logs": List[str],
      "state": Dict,
      "coherence_ratio": float,
      "psvchecksum": float
  }
  ```
- Persist the `state` dictionary returned by the `run()` method between runs.
- Use `quantic_processor.QuanticProcessor` for the Quantic runtime if you need numeric PSV behavior.

## Deployment
Follow DEPLOYMENT.md for staged rollout and MONITORING.md for metrics and runbook.
