terraform {
  required_version = ">= 1.8.0, < 2.0.0"

  backend "s3" {}

  required_providers {
    time = {
      source  = "hashicorp/time"
      version = "~> 0.13.0"
    }
  }
}
