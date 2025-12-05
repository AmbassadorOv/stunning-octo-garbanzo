import pytest
from omnigatesgl import omnigaterun, AL231_FIDELITY

def test_hero_correction_trigger():
    # input that yields zero depth -> unity 0 -> hero correction path
    result = omnigaterun("", incoming_state={'exp_unity': 0.0, 'count': 0})
    assert result['finalfidelity'] == AL231_FIDELITY
    assert "HERO-CORRECTION" in "".join(result['logs'])

def test_learning_path_updates_ema():
    sample = ""  # This input triggers HERO-CORRECTION, which activates the learning path
    r1 = omnigaterun(sample, incoming_state={'exp_unity': 0.0, 'count': 0})
    assert 'state' in r1 and 'exp_unity' in r1['state']
    r2 = omnigaterun(sample, incoming_state=r1['state'])
    assert r2['state']['count'] == r1['state']['count'] + 1
    assert r2['state']['exp_unity'] != r1['state']['exp_unity']

def test_coherence_ratio_bounds():
    sample = "אמתסודשקרכףעץחיה"
    r = omnigaterun(sample)
    assert 0.0 <= r['coherenceratio'] <= 10.0  # sanity bound
