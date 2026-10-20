locals {
  common_tags = {
    Project     = var.project_prefix
    Environment = var.environment
    ManagedBy   = "OpenTofu"
    Workshop    = "hands-on"
  }

  bucket_names = {
    for key, bucket in var.buckets :
    key => "${var.project_prefix}-${var.environment}-${key}"
  }
}
