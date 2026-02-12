import os
import json
import pytest
from unittest.mock import MagicMock, patch
from src.s3_multipart_upload import SovereignUploader, STATE_FILE

@pytest.fixture
def mock_s3():
    with patch('boto3.client') as mock_client:
        yield mock_client

@pytest.fixture
def cleanup_state():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    yield
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

def test_upload_init(mock_s3):
    uploader = SovereignUploader("test-bucket")
    assert uploader.bucket_name == "test-bucket"

def test_calculate_sha256():
    from src.s3_multipart_upload import calculate_sha256
    with open("test_file.txt", "w") as f:
        f.write("hello world")

    sha = calculate_sha256("test_file.txt")
    assert len(sha) == 64
    os.remove("test_file.txt")

def test_upload_file_new(mock_s3, cleanup_state):
    client_instance = mock_s3.return_value
    client_instance.create_multipart_upload.return_value = {"UploadId": "123"}
    client_instance.upload_part.return_value = {"ETag": "abc"}

    uploader = SovereignUploader("test-bucket")

    with open("test_file.bin", "wb") as f:
        f.write(os.urandom(1024))

    success = uploader.upload_file("test_file.bin")

    assert success is True
    client_instance.create_multipart_upload.assert_called_once()
    client_instance.complete_multipart_upload.assert_called_once()

    os.remove("test_file.bin")

def test_resume_logic(mock_s3, cleanup_state):
    client_instance = mock_s3.return_value

    # Pre-populate state
    state = {
        "test_file.bin": {
            "upload_id": "123",
            "parts": [{"PartNumber": 1, "ETag": "abc"}]
        }
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

    uploader = SovereignUploader("test-bucket")

    # File size > 1 part (50MB) to trigger more parts
    # But for mock test we can just check if it skips part 1
    with open("test_file.bin", "wb") as f:
        f.write(os.urandom(1024)) # Small file but state says part 1 done

    uploader.upload_file("test_file.bin")

    # Should NOT call create_multipart_upload
    client_instance.create_multipart_upload.assert_not_called()

    os.remove("test_file.bin")
