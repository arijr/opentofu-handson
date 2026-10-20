variable "policy_name" {
  description = "Nome lógico usado no documento de policy."
  type        = string
}

variable "statements" {
  description = "Declarações de exemplo para construir um documento JSON local."
  type = list(object({
    effect    = string
    actions   = list(string)
    resources = list(string)
  }))

  validation {
    condition     = alltrue([for statement in var.statements : contains(["Allow", "Deny"], statement.effect)])
    error_message = "Cada declaração deve usar Effect Allow ou Deny."
  }
}
