// AWS PROVIDER (LOCALSTACK)
provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_force_path_style = true

  endpoints {
    dynamodb = "http://localhost:4566"
    lambda   = "http://localhost:4566"
    kinesis  = "http://localhost:4566"
    s3  = "http://localhost:4566"
  }
}

// DYNAMODB TABLES
resource "aws_dynamodb_table" "demo-dynamodb-tf" {
  name           = "demo-dynamodb-tf"
  read_capacity  = "20"
  write_capacity = "20"
  hash_key       = "ID"

  attribute {
    name = "ID"
    type = "S"
  }
}

// S3
resource "aws_s3_bucket" "demo-bucket-tf" {
  bucket = "demo-bucket-tf"
  acl    = "public-read"
}