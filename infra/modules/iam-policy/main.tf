locals {
  policy_document = {
    Id      = var.policy_name
    Version = "2012-10-17"
    Statement = [for statement in var.statements : {
      Effect   = statement.effect
      Action   = statement.actions
      Resource = statement.resources
    }]
  }
}
