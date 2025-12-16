resource "random_id" "suffix" {
  count       = 2
  byte_length = 6
}

module "east" {
  source             = "./modules/s3_bucket"
  bucket_name_prefix = var.bucket_name_prefix
  region             = var.regions[0]
  random_suffix      = random_id.suffix[0].hex
}

module "west" {
  source = "./modules/s3_bucket"
  providers = { aws = aws.us_west_2 }
  bucket_name_prefix = var.bucket_name_prefix
  region             = var.regions[1]
  random_suffix      = random_id.suffix[1].hex
  lifecycle_days     = 30
}
