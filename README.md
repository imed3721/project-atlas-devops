# Project Atlas — AWS DevOps Project

## Overview

Project Atlas demonstrates a browser-based DevOps workflow using GitHub Actions, Terraform, AWS Lambda, IAM OpenID Connect (OIDC), and Amazon CloudWatch.

The project covers automated testing, infrastructure deployment, application health checks, monitoring, drift detection, and failure recovery.

## Architecture

GitHub repository → GitHub Actions → OIDC → AWS IAM → Terraform → AWS Lambda → Amazon CloudWatch.

Terraform state is stored remotely in Amazon S3.

## Application and Unit Tests

The Python application provides a health-check endpoint. Unit tests verify the expected application response before deployment.

Relevant files:

- `app/handler.py`
- `app/test_handler.py`

### Application source code

![Application source code](docs/screenshots/screenshot-03-source-code.png)

## Continuous Integration

GitHub Actions automatically runs Python unit tests and validates the Terraform configuration.

### CI workflow

![CI workflow](docs/screenshots/screenshot-04-ci-pipeline.png)

## Secure GitHub-to-AWS Authentication

GitHub Actions uses OpenID Connect to obtain temporary AWS credentials through an IAM role rather than storing long-lived AWS access keys in GitHub.

The IAM trust policy restricts which GitHub repository and environment can assume the role.

### OIDC configuration

![OIDC configuration](docs/screenshots/screenshot-06-oidc.png)

### GitHub environment

![GitHub environment](docs/screenshots/screenshot-07-github-environment.png)

## Terraform Infrastructure and Remote State

Terraform defines the AWS infrastructure. The remote state file is stored in an Amazon S3 bucket, with versioning and state locking configured.

### Terraform state bucket

![Terraform state bucket](docs/screenshots/screenshot-08-state-bucket.png)

### Terraform configuration

![Terraform configuration](docs/screenshots/screenshot-09-terraform-configuration.png)

## Automated Deployment

The deployment workflow authenticates to AWS using OIDC, validates the Terraform configuration, generates a plan, and applies the infrastructure changes.

### Deployment workflow

![Deployment workflow](docs/screenshots/screenshot-10-deployment-workflow.png)

### AWS identity verification

![AWS identity verification](docs/screenshots/screenshot-11-aws-identity.png)

### Terraform outputs

![Terraform outputs](docs/screenshots/screenshot-12-terraform-outputs.png)

## Application Health Check

The deployed Lambda Function URL is tested in a browser to verify that the application responds successfully.

The demonstration endpoint is publicly accessible and is not intended for sensitive production workloads.

### Health-check response

![Health-check response](docs/screenshots/screenshot-13-health-check.png)

## Monitoring and Observability

Amazon CloudWatch collects Lambda logs and provides an alarm to monitor function errors.

### CloudWatch logs

![CloudWatch logs](docs/screenshots/screenshot-14-cloudwatch-logs.png)

### CloudWatch alarm

![CloudWatch alarm](docs/screenshots/screenshot-15-cloudwatch-alarm.png)

## Infrastructure Drift Detection

Terraform drift detection identifies differences between the declared infrastructure configuration and the live AWS resources.

A manual change is introduced in the AWS Console, detected by the drift workflow, and reconciled through Terraform.

### Drift introduced

![Drift introduced](docs/screenshots/screenshot-16-drift-introduced.png)

### Drift detected

![Drift detected](docs/screenshots/screenshot-17-drift-detected.png)

### Drift resolved

![Drift resolved](docs/screenshots/screenshot-18-drift-resolved.png)

## Failure Testing and Recovery

A unit test is deliberately changed to produce a failure. The CI workflow detects the failure, and the test is restored to confirm that the pipeline can pass again.

### CI failure

![CI failure](docs/screenshots/screenshot-19-ci-failure.png)

### CI recovery

![CI recovery](docs/screenshots/screenshot-20-ci-recovered.png)

## Security and Future Improvements

Potential improvements include:

- Enforcing least-privilege IAM permissions.
- Requiring approval before applying production infrastructure changes.
- Pinning GitHub Actions to verified commit SHAs.
- Adding latency and application-level monitoring.
- Documenting state recovery and incident response procedures.
- Reviewing endpoint authentication before any production use.

## Skills Demonstrated

- GitHub and repository management
- Python and unit testing
- GitHub Actions CI/CD
- AWS IAM and OpenID Connect
- Terraform Infrastructure as Code
- Amazon S3 remote state
- AWS Lambda deployment
- Amazon CloudWatch logs and alarms
- Infrastructure drift detection
- Failure testing and recovery
- Technical documentation

## Cost Awareness

AWS charges may apply depending on usage, region, and account pricing. Budget notifications do not impose a hard spending limit.

Resources that are no longer needed should be removed carefully. Preserve Terraform state until it is no longer required for recovery or infrastructure management.
