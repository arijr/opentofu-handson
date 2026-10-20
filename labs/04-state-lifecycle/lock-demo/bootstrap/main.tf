resource "aws_s3_bucket" "state" {
  bucket = "tofu-workshop-lock-state"

  tags = {
    Project   = "tofu-workshop"
    Purpose   = "backend-lock-demo"
    ManagedBy = "OpenTofu"
  }
}

output "state_bucket" {
  description = "Bucket local do Floci usado somente na demonstração de locking."
  value       = aws_s3_bucket.state.id
}
