import boto3
import hashlib
import sys
import os
from boto3.s3.transfer import TransferConfig

def calculate_sha256(file_path):
    """Calculates the SHA256 hash of a file for integrity verification."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def sovereign_upload(file_path, bucket, key):
    """
    Performs a Sovereign Upload: Parallel multipart upload with SHA256 metadata injection.
    This is the 'Final Nexus' bridge between local audit and the Sovereign Cloud.
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

    print(f"--- 🌀 SOVEREIGN UPLOAD INITIATED ---")

    # 1. The Oracle Calculation (SHA256)
    print(f"Calculating integrity hash (The Oracle Check)...")
    sha256 = calculate_sha256(file_path)
    print(f"✅ SHA256: {sha256}")

    # 2. Configure AWS S3 Client
    s3 = boto3.client('s3')

    # 3. Parallel Multipart Configuration
    # We use a 5MB threshold and 10 threads for parallel execution
    config = TransferConfig(
        multipart_threshold=5 * 1024 * 1024,
        max_concurrency=10,
        use_threads=True
    )

    extra_args = {
        'Metadata': {
            'sha256': sha256,
            'deployment-epoch': '3',
            'governance-status': 'sealed'
        }
    }

    # 4. Execution of the Descent (Upload)
    try:
        print(f"Uploading to s3://{bucket}/{key} in parallel units...")
        s3.upload_file(
            file_path,
            bucket,
            key,
            ExtraArgs=extra_args,
            Config=config
        )
        print(f"--- ✅ SOVEREIGN UPLOAD COMPLETE ---")
        print(f"Metadata injected: x-amz-meta-sha256={sha256}")
    except Exception as e:
        print(f"❌ CRITICAL FAILURE during Sovereign Upload: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python sovereign_upload.py <file_path> <bucket> <key>")
        sys.exit(1)

    target_file = sys.argv[1]
    target_bucket = sys.argv[2]
    target_key = sys.argv[3]

    sovereign_upload(target_file, target_bucket, target_key)
