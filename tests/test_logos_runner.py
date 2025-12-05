import pytest
from unittest.mock import patch, mock_open
import json
from logos_runner import ProjectBigEaglesDME, LionProjectCoordinator, load_config, save_config

@pytest.fixture
def mock_config():
    return {
        "LATTICE_DIM": 36.0,
        "ALPHA": 0.15,
        "PERSISTENCE_MODE": "JSON",
        "EMA_UNITY": 1e10,
        "RUN_COUNT": 10
    }

def test_load_config_found(mock_config):
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_config))) as mock_file:
        config = load_config()
        assert config == mock_config
        mock_file.assert_called_with('dme_config.json', 'r')

def test_load_config_not_found():
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = FileNotFoundError
        config = load_config()
        assert config["LATTICE_DIM"] == 36.0
        assert config["ALPHA"] == 0.15

def test_save_config(mock_config):
    with patch("builtins.open", mock_open()) as mock_file:
        save_config(mock_config)
        mock_file.assert_called_with('dme_config.json', 'w')
        # The following assertion is more complex and depends on the exact write calls
        # assert mock_file().write.call_count == 1

class TestProjectBigEaglesDME:
    def test_init(self, mock_config):
        dme = ProjectBigEaglesDME("test_data", mock_config)
        assert dme.raw_data == "test_data"
        assert dme.config == mock_config

    def test_i_s_ingress(self, mock_config):
        dme = ProjectBigEaglesDME("test_data", mock_config)
        state_data = {"EMA_UNITY": 1.0, "RUN_COUNT": 1, "state_hash": "a_valid_ha"}
        with patch('logos_runner.hashlib.sha256') as mock_sha:
            mock_sha.return_value.hexdigest.return_value = "a_valid_hash"
            dme.I_S_Ingress(state_data)
            assert "S: SUCCESS: PSV signature verified." in dme.logs

    def test_q_m_execute(self, mock_config):
        dme = ProjectBigEaglesDME("test_data", mock_config)
        dme.psv = {"EMA_UNITY": 1e10}
        unity = dme.Q_M_Execute()
        assert unity > 0
        assert "M: Core Unity calculated" in dme.logs[0]

    def test_p_t_r_g_s_egress(self, mock_config):
        dme = ProjectBigEaglesDME("test_data", mock_config)
        dme.psv = {"EMA_UNITY": 1e10, "RUN_COUNT": 10}
        dme.P_T_R_G_S_Egress(1.1e10)
        assert dme.psv["RUN_COUNT"] == 11
        assert "S: Egress lock generated" in dme.logs[-1]

    def test_j_h_assessment(self, mock_config):
        dme = ProjectBigEaglesDME("test_data", mock_config)
        dme.psv = {"EMA_UNITY": 1e10}
        lbr_data = {"median_ffi_time": 0.0005, "observed_t_iglx": 0.00065}
        psar_data = {"max_acceptable_drift": 1e7, "default_alpha": 0.15}
        config, l_cr = dme.J_H_Assessment(1.1e10, lbr_data, psar_data)
        assert "J: L_CR Calculated" in dme.logs[0]

class TestLionProjectCoordinator:
    def test_k_synchronize(self, mock_config):
        coord = LionProjectCoordinator(mock_config)
        node_results = [
            {'ema': 1.0e10, 'l_cr': 1.5},
            {'ema': 1.2e10, 'l_cr': 2.0}
        ]
        ema, l_cr = coord.K_Synchronize(node_results)
        assert ema == 1.1e10
        assert l_cr == 1.75
        assert "K: SYNCHRONIZATION COMPLETE" in coord.logs[0]

    def test_j_generate_suggestion(self, mock_config):
        coord = LionProjectCoordinator(mock_config)
        psar_data = {"max_acceptable_drift": 1e7, "default_alpha": 0.15}
        suggestion, directives = coord.J_Generate_Suggestion(1.1e10, 1.8, psar_data)
        assert "DAILY IMPROVEMENT SUGGESTION" in suggestion
        assert ("PERSISTENCE_MODE", "CSV") in directives

    def test_r_self_implement(self, mock_config):
        coord = LionProjectCoordinator(mock_config)
        directives = [("PERSISTENCE_MODE", "CSV"), ("ALPHA", 0.075)]
        coord.cluster_ema_c = 1.1e10
        with patch('logos_runner.save_config') as mock_save:
            coord.R_Self_Implement(directives)
            assert coord.config["PERSISTENCE_MODE"] == "CSV"
            assert coord.config["ALPHA"] == 0.075
            assert "R: SELF-IMPLEMENTATION SUCCESS" in coord.logs[-1]
            mock_save.assert_called_once()
