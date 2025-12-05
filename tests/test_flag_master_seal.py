import pytest
from src.flag_master_seal import TransparentLayerFlag, A_Neshama, B_Guf, C_Levush, D_Heichal

def test_get_frequency():
    assert TransparentLayerFlag.get_frequency("ATZILUT") == 4.0
    assert TransparentLayerFlag.get_frequency("BERIAH") == 3.0
    assert TransparentLayerFlag.get_frequency("YETZIRAH") == 2.0
    assert TransparentLayerFlag.get_frequency("ASSIAH") == 1.0
    assert TransparentLayerFlag.get_frequency("UNKNOWN") == 1.0

def test_calculate_action_estimate():
    neshama = A_Neshama("ATZILUT")
    guf = B_Guf("ATZILUT")
    levush = C_Levush("ATZILUT")
    heichal = D_Heichal("ATZILUT")

    assert neshama._calculate_action_estimate(0.8) == pytest.approx(0.512)
    assert guf._calculate_action_estimate(0.8) == pytest.approx(0.8)
    assert levush._calculate_action_estimate(0.8) == pytest.approx(0.64)
    assert heichal._calculate_action_estimate(0.8) == pytest.approx(1.0)
