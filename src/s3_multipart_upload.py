import os
import json
import hashlib
import boto3
from botocore.exceptions import ClientError

CHUNK_SIZE = 50 * 1024 * 1024  # 50MB
STATE_FILE = "state.json"

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

class SovereignUploader:
    def __init__(self, bucket_name, region_name="us-east-1"):
        self.s3_client = boto3.client("s3", region_name=region_name)
        self.bucket_name = bucket_name

    def load_state(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_state(self, state):
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)

    def upload_file(self, file_path, object_name=None):
        if object_name is None:
            object_name = os.path.basename(file_path)

        file_size = os.path.getsize(file_path)
        file_sha256 = calculate_sha256(file_path)

        state = self.load_state()
        upload_id = state.get(file_path, {}).get("upload_id")
        parts = state.get(file_path, {}).get("parts", [])

        if not upload_id:
            try:
                response = self.s3_client.create_multipart_upload(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Metadata={"sha256": file_sha256}
                )
                upload_id = response["UploadId"]
                state[file_path] = {"upload_id": upload_id, "parts": []}
                self.save_state(state)
            except ClientError as e:
                print(f"Error starting multipart upload: {e}")
                return False

        print(f"Starting/Resuming upload for {file_path} (UploadId: {upload_id})")

        try:
            with open(file_path, "rb") as f:
                part_number = len(parts) + 1
                f.seek(len(parts) * CHUNK_SIZE)

                while True:
                    data = f.read(CHUNK_SIZE)
                    if not data:
                        break

                    print(f"Uploading part {part_number}...")
                    response = self.s3_client.upload_part(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        Body=data
                    )

                    parts.append({"PartNumber": part_number, "ETag": response["ETag"]})
                    state[file_path]["parts"] = parts
                    self.save_state(state)
                    part_number += 1

            print("Completing multipart upload...")
            self.s3_client.complete_multipart_upload(
                Bucket=self.bucket_name,
                Key=object_name,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts}
            )

            # Clean up state for this file
            del state[file_path]
            self.save_state(state)
            print(f"Upload successful: {object_name}")
            return True

        except ClientError as e:
            print(f"Error during multipart upload: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python s3_multipart_upload.py <bucket_name> <file_path>")
    else:
        uploader = SovereignUploader(sys.argv[1])
        uploader.upload_file(sys.argv[2])
