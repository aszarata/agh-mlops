output "bucket_arns" {
  value = {
    east = aws_s3_bucket.east.arn
    west = aws_s3_bucket.west.arn
  }
}
