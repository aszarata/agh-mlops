resource "aws_s3_bucket" "east" {
  bucket = "unique-bucket-east-123"
}

resource "aws_s3_bucket" "west" {
  bucket   = "unique-bucket-west-123"
  provider = aws.us_west_2
}
