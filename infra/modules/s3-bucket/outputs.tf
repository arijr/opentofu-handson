output "bucket_name" {
  description = "Nome do bucket criado."
  value       = aws_s3_bucket.this.id
}

output "bucket_arn" {
  description = "ARN atribuído pelo provider ao bucket."
  value       = aws_s3_bucket.this.arn
}
