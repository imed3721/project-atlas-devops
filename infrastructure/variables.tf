variable "aws_region" {
  description = "AWS region where Project Atlas resources are deployed"
  type        = string
  default     = "eu-west-2"
}

variable "project_name" {
  description = "Prefix used to name Project Atlas resources"
  type        = string
  default     = "project-atlas"
}

variable "app_version" {
  description = "Version of the application deployed by CI/CD"
  type        = string
  default     = "1.0.0"
}
