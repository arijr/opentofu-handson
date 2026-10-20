module "s3_bucket" {
  source   = "./modules/s3-bucket"
  for_each = local.bucket_names

  bucket_name = each.value
  purpose     = var.buckets[each.key].purpose
  tags        = local.common_tags
}
