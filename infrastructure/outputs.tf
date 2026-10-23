output "function_name" {
  description = "Name of the deployed AWS Lambda function"
  value       = aws_lambda_function.application.function_name
}

output "function_url" {
  description = "Public URL of the Project Atlas health API"
  value       = aws_lambda_function_url.application.function_url
}

output "log_group_name" {
  description = "Name of the CloudWatch log group for the Lambda function"
  value       = aws_cloudwatch_log_group.application.name
}
