output "policy_json" {
  description = "Documento de policy JSON produzido localmente; não cria policy IAM."
  value       = jsonencode(local.policy_document)
}
