resource "random_id" "suffix" {
  count       = 2
  byte_length = 4
}

resource "aws_s3_bucket" "east" {
  bucket = "${var.bucket_name_prefix}-east-${random_id.suffix[0].hex}"
}

resource "aws_s3_bucket_versioning" "east" {
  bucket = aws_s3_bucket.east.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_lifecycle_configuration" "east" {
  bucket = aws_s3_bucket.east.id
  rule {
    id     = "glacier"
    status = "Enabled"
    transition {
      days          = 90
      storage_class = "GLACIER_IR"
    }
  }
}

resource "aws_s3_bucket" "west" {
  bucket   = "${var.bucket_name_prefix}-west-${random_id.suffix[1].hex}"
  provider = aws.us_west_2
}
