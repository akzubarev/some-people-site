"""Upload a PostgreSQL dump to the configured private OCI Object Storage bucket."""

import hashlib
import os
import sys
from pathlib import Path

import boto3
from botocore.config import Config


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: upload-database-backup.py /backup/file.dump object-key")
    path = Path(sys.argv[1])
    key = sys.argv[2]
    if not path.is_file() or not key.startswith("database-backups/"):
        raise SystemExit("Invalid backup path or object key")

    bucket = os.environ["MEDIA_S3_BUCKET"]
    client = boto3.client(
        "s3",
        endpoint_url=os.environ["MEDIA_S3_ENDPOINT_URL"],
        region_name=os.environ["MEDIA_S3_REGION"],
        aws_access_key_id=os.environ["MEDIA_S3_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["MEDIA_S3_SECRET_ACCESS_KEY"],
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": "path", "payload_signing_enabled": True},
            request_checksum_calculation="when_required",
            response_checksum_validation="when_required",
        ),
    )
    digest = sha256_file(path)
    with path.open("rb") as source:
        client.put_object(
            Bucket=bucket,
            Key=key,
            Body=source,
            Metadata={"sha256": digest},
            ContentType="application/octet-stream",
        )

    remote = client.get_object(Bucket=bucket, Key=key)
    remote_digest = hashlib.sha256()
    for chunk in remote["Body"].iter_chunks(chunk_size=1024 * 1024):
        remote_digest.update(chunk)
    if remote_digest.hexdigest() != digest or remote["ContentLength"] != path.stat().st_size:
        raise SystemExit("Remote database backup verification failed")
    print(f"Verified private Object Storage backup: {key} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
