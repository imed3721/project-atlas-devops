variable "aws_region" {
  description = "AWS region where Project Atlas resources are deployed"
  type        = string
  default     = "eu-west-2"
}

variable "project_name" {
  description = "Name used for Project Atlas AWS resources"
  type        = string
  default     = "project-atlas"
}

variable "app_version" {
  description = "Application version exposed by the Lambda health endpoint"
  type        = string
  default     = "dev"
}
