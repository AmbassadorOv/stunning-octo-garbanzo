# Project Big Eagles: LOGOS Runner

This project implements the master automation component for Project Big Eagles, the LOGOS Runner. It encapsulates the entire `X -> I -> S -> L -> Q -> M -> P -> T -> R -> G -> S -> J -> H -> A` LOGOS sequence.

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
python logos_runner.py
```
The script will create a `dme_config.json` file on its first run, which it will then use to store and manage its state.

## Run tests
```bash
PYTHONPATH=. pytest -q
```

## Architecture
The project is divided into two main components:
- `ProjectBigEaglesDME`: The core DME, responsible for executing the main LOGOS sequence.
- `LionProjectCoordinator`: The coordinator, responsible for synchronizing results from distributed nodes and generating and implementing daily improvement suggestions.

## Deployment
Follow DEPLOYMENT.md for staged rollout and MONITORING.md for metrics and runbook.
