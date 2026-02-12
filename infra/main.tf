provider "aws" {
  region = "us-east-1"
}

resource "aws_kms_key" "sovereign_master_key" {
  description             = "KMS key for encrypting Sovereign Audit Trails"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  tags = {
    Name = "sovereign-master-key"
  }
}

resource "aws_kms_alias" "sovereign_master_key_alias" {
  name          = "alias/sovereign-master-key"
  target_key_id = aws_kms_key.sovereign_master_key.key_id
}

resource "aws_s3_bucket" "sovereign_vault" {
  bucket = "sovereign-vault"

  object_lock_enabled = true

  tags = {
    Name = "sovereign-vault"
  }
}

resource "aws_s3_bucket_versioning" "sovereign_vault_versioning" {
  bucket = aws_s3_bucket.sovereign_vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "sovereign_vault_encryption" {
  bucket = aws_s3_bucket.sovereign_vault.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.sovereign_master_key.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "sovereign_vault_access" {
  bucket = aws_s3_bucket.sovereign_vault.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
