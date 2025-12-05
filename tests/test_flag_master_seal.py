import pytest
from src.flag_master_seal import TransparentLayerFlag, C_Neshama, D_Guf, E_Levush, F_Heichal

def test_get_frequency():
    assert TransparentLayerFlag.get_frequency("ATZILUT") == 4.0
    assert TransparentLayerFlag.get_frequency("BERIAH") == 3.0
    assert TransparentLayerFlag.get_frequency("YETZIRAH") == 2.0
    assert TransparentLayerFlag.get_frequency("ASSIAH") == 1.0
    assert TransparentLayerFlag.get_frequency("UNKNOWN") == 1.0

def test_get_cf():
    assert TransparentLayerFlag.get_cf('A') == 3
    assert TransparentLayerFlag.get_cf('B') == 1
    assert TransparentLayerFlag.get_cf('C') == 2
    assert TransparentLayerFlag.get_cf('D') == 0
    assert TransparentLayerFlag.get_cf('UNKNOWN') == 0

def test_calculate_action_estimate():
    neshama = C_Neshama("ATZILUT")
    guf = D_Guf("ATZILUT")
    levush = E_Levush("ATZILUT")
    heichal = F_Heichal("ATZILUT")

    assert neshama._calculate_action_estimate(0.8) == pytest.approx(0.512)
    assert guf._calculate_action_estimate(0.8) == pytest.approx(0.8)
    assert levush._calculate_action_estimate(0.8) == pytest.approx(0.64)
    assert heichal._calculate_action_estimate(0.8) == pytest.approx(1.0)
