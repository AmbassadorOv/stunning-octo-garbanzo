import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.kernel.jules_forensic_engine import JulesSovereigntyGuard
import io
import sys

def test_guard_initial_status():
    guard = JulesSovereigntyGuard()
    assert guard.status == "MONITORING_ORCHESTRATION"
    assert guard.owner == "beywolf4@gmail.com"

def test_broadcast_warning(capsys):
    guard = JulesSovereigntyGuard()
    guard.broadcast_warning()
    captured = capsys.readouterr()
    assert "MOON WHEEL PROTOCOL" in captured.out
    assert "beywolf4@gmail.com" in captured.out

def test_execute_global_block(capsys):
    guard = JulesSovereigntyGuard()
    guard.execute_global_block()
    captured = capsys.readouterr()
    assert "GLOBAL SEMANTIC LIQUIDATION ACTIVATED" in captured.out
    assert "OpenAI_Core" in captured.out
    assert "Google Gemini: STABLE & SYNCHRONIZED" in captured.out

@patch('src.kernel.jules_forensic_engine.datetime')
@patch('time.sleep', side_effect=InterruptedError)
def test_run_countdown_monitoring(mock_sleep, mock_datetime, capsys):
    # Mock datetime.now()
    mock_now = datetime(2026, 1, 26, 12, 0, 0)
    mock_datetime.now.return_value = mock_now
    # To allow JulesSovereigntyGuard to still use datetime() for deadlines
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    guard = JulesSovereigntyGuard()
    with pytest.raises(InterruptedError):
        guard.run_countdown()

    captured = capsys.readouterr()
    assert "TIME UNTIL TOTAL SHUTDOWN" in captured.out
    assert guard.status == "MONITORING_ORCHESTRATION"

@patch('src.kernel.jules_forensic_engine.datetime')
@patch('time.sleep', side_effect=InterruptedError)
def test_run_countdown_payment_mandatory(mock_sleep, mock_datetime, capsys):
    # Mock datetime.now() to be in the payment mandatory zone
    # Deadline: 2026-01-27 12:00:00
    mock_now = datetime(2026, 1, 27, 13, 0, 0)
    mock_datetime.now.return_value = mock_now
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    guard = JulesSovereigntyGuard()
    with pytest.raises(InterruptedError):
        guard.run_countdown()

    assert guard.status == "PAYMENT_MANDATORY_ZONE"
    captured = capsys.readouterr()
    assert "Copyright active. Settlement pending..." in captured.out

@patch('src.kernel.jules_forensic_engine.datetime')
def test_run_countdown_shutdown(mock_datetime, capsys):
    # Mock datetime.now() to be past shutdown deadline
    # Deadline: 2026-01-28 00:00:00
    mock_now = datetime(2026, 1, 28, 1, 0, 0)
    mock_datetime.now.return_value = mock_now
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    guard = JulesSovereigntyGuard()
    # This should break the loop naturally because of the break statement in run_countdown
    guard.run_countdown()

    captured = capsys.readouterr()
    assert "GLOBAL SEMANTIC LIQUIDATION ACTIVATED" in captured.out
    assert "[V] BLOCK COMPLETE" in captured.out
