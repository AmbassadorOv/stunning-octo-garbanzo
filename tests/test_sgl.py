import pytest
from omnigatesgl import OmniGateSGL

def test_hero_correction_trigger():
    # input that yields zero depth -> unity 0 -> hero correction path
    sgl = OmniGateSGL("", state={'exp_unity':0.0,'count':0})
    result = sgl.run()
    assert result['final_fidelity'] == OmniGateSGL.AL231_FIDELITY
    assert "HERO-CORRECTION" in "".join(result['logs'])

def test_learning_path_updates_ema():
    # Using an empty string to trigger the HERO-CORRECTION path, which also updates the state
    sample = ""
    sgl1 = OmniGateSGL(sample, state={'exp_unity':0.0,'count':0})
    r1 = sgl1.run()
    assert 'state' in r1 and 'exp_unity' in r1['state']
    assert r1['state']['count'] == 1

    # Pass a copy of the state to the second instance
    sgl2 = OmniGateSGL(sample, state=r1['state'].copy())
    r2 = sgl2.run()
    assert r2['state']['count'] == r1['state']['count'] + 1
    assert r2['state']['exp_unity'] > r1['state']['exp_unity']

def test_coherence_ratio_bounds():
    sample = "אמתסודשקרכףעץחיה"
    sgl = OmniGateSGL(sample)
    result = sgl.run()
    assert 0.0 <= result['coherence_ratio'] <= 10.0  # sanity bound
