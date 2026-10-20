variable "bucket_name" {
  description = "Nome do bucket S3."
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$", var.bucket_name))
    error_message = "O nome deve ter de 3 a 63 caracteres minúsculos, números e hífens."
  }
}

variable "purpose" {
  description = "Finalidade didática do bucket."
  type        = string
}

variable "tags" {
  description = "Tags comuns definidas pelo módulo raiz."
  type        = map(string)
  default     = {}
}
