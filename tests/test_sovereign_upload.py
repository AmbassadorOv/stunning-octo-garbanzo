import pytest
import os
import hashlib
from unittest.mock import MagicMock, patch
from src.sovereign_upload import calculate_sha256, sovereign_upload

def test_calculate_sha256(tmp_path):
    # Create a dummy file
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "hello.txt"
    content = b"Sovereign integrity check"
    p.write_bytes(content)

    expected_hash = hashlib.sha256(content).hexdigest()
    assert calculate_sha256(str(p)) == expected_hash

@patch('boto3.client')
def test_sovereign_upload_success(mock_boto_client, tmp_path):
    # Setup mock
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3

    # Create a dummy file
    p = tmp_path / "audit.tar.gz"
    p.write_bytes(b"dummy bundle")

    # Run upload
    sovereign_upload(str(p), "my-bucket", "my-key")

    # Verify s3.upload_file was called
    mock_s3.upload_file.assert_called_once()
    args, kwargs = mock_s3.upload_file.call_args

    assert args[0] == str(p)
    assert args[1] == "my-bucket"
    assert args[2] == "my-key"
    assert 'Metadata' in kwargs['ExtraArgs']
    assert 'sha256' in kwargs['ExtraArgs']['Metadata']
    assert kwargs['ExtraArgs']['Metadata']['deployment-epoch'] == '3'

@patch('boto3.client')
def test_sovereign_upload_failure(mock_boto_client, tmp_path):
    # Setup mock to raise exception
    mock_s3 = MagicMock()
    mock_s3.upload_file.side_effect = Exception("S3 Upload Failed")
    mock_boto_client.return_value = mock_s3

    # Create a dummy file
    p = tmp_path / "audit.tar.gz"
    p.write_bytes(b"dummy bundle")

    # Run upload and expect exit
    with pytest.raises(SystemExit) as e:
        sovereign_upload(str(p), "my-bucket", "my-key")
    assert e.value.code == 1
