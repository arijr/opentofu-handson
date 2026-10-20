variable "aws_endpoint" {
  description = "Endpoint HTTP local do Floci. Endpoints remotos não são permitidos."
  type        = string
  default     = "http://localhost:4566"

  validation {
    condition     = can(regex("^http://(localhost|127\\.0\\.0\\.1):4566$", var.aws_endpoint))
    error_message = "Use somente http://localhost:4566 ou http://127.0.0.1:4566."
  }
}

variable "aws_region" {
  description = "Região usada para nomes e respostas no Floci."
  type        = string
  default     = "us-east-1"

  validation {
    condition     = var.aws_region == "us-east-1"
    error_message = "Este laboratório usa exclusivamente a região us-east-1."
  }
}

variable "project_prefix" {
  description = "Prefixo minúsculo e válido para os nomes dos buckets."
  type        = string
  default     = "tofu-workshop"

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]{1,19}[a-z0-9]$", var.project_prefix))
    error_message = "Use de 3 a 21 caracteres: letras minúsculas, números e hífens; comece e termine com letra ou número."
  }
}

variable "environment" {
  description = "Identificador do ambiente incluído nas tags e nos nomes."
  type        = string
  default     = "dev"

  validation {
    condition     = can(regex("^[a-z0-9-]{2,12}$", var.environment))
    error_message = "Use de 2 a 12 caracteres minúsculos, números ou hífens."
  }
}

variable "buckets" {
  description = "Buckets adicionais nomeados por chave estável. A chave integra o nome do bucket."
  type = map(object({
    purpose = string
  }))
  default = {
    artifacts = {
      purpose = "artefatos de laboratorio"
    }
  }

  validation {
    condition = (
      length(var.buckets) <= 4 &&
      alltrue([
        for key in keys(var.buckets) :
        can(regex("^[a-z0-9][a-z0-9-]{0,14}[a-z0-9]$", key))
      ])
    )
    error_message = "Informe no máximo quatro chaves de 2 a 16 caracteres, em minúsculas, números ou hífens."
  }
}
