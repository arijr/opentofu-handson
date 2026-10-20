output "bucket_names" {
  description = "Nomes dos buckets S3 criados pelo módulo."
  value       = { for key, bucket in module.s3_bucket : key => bucket.bucket_name }
}

output "bucket_arns" {
  description = "ARNs simulados dos buckets S3."
  value       = { for key, bucket in module.s3_bucket : key => bucket.bucket_arn }
}

output "local_endpoint" {
  description = "Endpoint usado pelo provider para as APIs AWS do laboratório."
  value       = var.aws_endpoint
}
