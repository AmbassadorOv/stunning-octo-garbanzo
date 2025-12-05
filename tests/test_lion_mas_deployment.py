import pytest
from src.lion_mas_deployment import deploy_lion_mas

def test_deploy_lion_mas():
    try:
        deploy_lion_mas()
    except Exception as e:
        pytest.fail(f"deploy_lion_mas() raised an exception: {e}")
