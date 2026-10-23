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

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/c915fe138e4fcbc31d172751fb85b72423a4196f/screenshots/Screenshot%202026-10-23%20at%2007.20.21.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/c915fe138e4fcbc31d172751fb85b72423a4196f/screenshots/Screenshot%202026-10-23%20at%2007.20.31.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/c915fe138e4fcbc31d172751fb85b72423a4196f/screenshots/Screenshot%202026-10-23%20at%2007.20.40.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/c915fe138e4fcbc31d172751fb85b72423a4196f/screenshots/Screenshot%202026-10-23%20at%2007.20.47.png)

## Continuous Integration

GitHub Actions automatically runs Python unit tests and validates the Terraform configuration.

### CI workflow

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/0bee79e836076e4f459e58f1d795b578e8d2cbe3/screenshots/Screenshot%202026-10-23%20at%2007.21.38.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/0bee79e836076e4f459e58f1d795b578e8d2cbe3/screenshots/Screenshot%202026-10-23%20at%2007.21.49.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/0bee79e836076e4f459e58f1d795b578e8d2cbe3/screenshots/Screenshot%202026-10-23%20at%2007.21.56.png)

## Secure GitHub-to-AWS Authentication

GitHub Actions uses OpenID Connect to obtain temporary AWS credentials through an IAM role rather than storing long-lived AWS access keys in GitHub.

The IAM trust policy restricts which GitHub repository and environment can assume the role.

### OIDC configuration

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/dca7719da5fcbea165ca6c7fe29861f7e4705042/screenshots/Screenshot%202026-10-23%20at%2007.41.13.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/dca7719da5fcbea165ca6c7fe29861f7e4705042/screenshots/Screenshot%202026-10-23%20at%2007.41.22.png)


## Terraform Infrastructure and Remote State

Terraform defines the AWS infrastructure. The remote state file is stored in an Amazon S3 bucket, with versioning and state locking configured.

### Terraform state bucket

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/dca7719da5fcbea165ca6c7fe29861f7e4705042/screenshots/Screenshot%202026-10-23%20at%2007.49.28.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/dca7719da5fcbea165ca6c7fe29861f7e4705042/screenshots/Screenshot%202026-10-23%20at%2007.49.39.png)

### Terraform configuration

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.54.43.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.54.49.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.54.54.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.55.03.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.55.37.png)


## Automated Deployment

The deployment workflow authenticates to AWS using OIDC, validates the Terraform configuration, generates a plan, and applies the infrastructure changes.

### Deployment workflow

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/40c2bf9903d3ccfa8396ef084a3a2f33c706c1f5/screenshots/screenshot%208.png)

### AWS identity verification

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/40c2bf9903d3ccfa8396ef084a3a2f33c706c1f5/screenshots/screenshot%209.png)

### Terraform outputs

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.11.49.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.11.59.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.12.07.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.12.15.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.12.24.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.12.30.png)

## Application Health Check

The deployed Lambda Function URL is tested in a browser to verify that the application responds successfully.

The demonstration endpoint is publicly accessible and is not intended for sensitive production workloads.

### Health-check response

![Health-check response](https://github.com/imed3721/project-atlas-devops/blob/bcd03361520df044f37848c880105b5118624409/screenshots/Screenshot%2011.png)

## Monitoring and Observability

Amazon CloudWatch collects Lambda logs and provides an alarm to monitor function errors.

### CloudWatch logs

![CloudWatch logs](https://github.com/imed3721/project-atlas-devops/blob/bcd03361520df044f37848c880105b5118624409/screenshots/screenshot%2012.png)

### CloudWatch alarm

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/81339602fac5affbb545545a9b137c132e21ee31/screenshots/Screenshot%202026-10-23%20at%2008.59.29.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/81339602fac5affbb545545a9b137c132e21ee31/screenshots/Screenshot%202026-10-23%20at%2008.59.10.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/81339602fac5affbb545545a9b137c132e21ee31/screenshots/Screenshot%202026-10-23%20at%2008.58.17.png)

## Infrastructure Drift Detection

Terraform drift detection identifies differences between the declared infrastructure configuration and the live AWS resources.

A manual change is introduced in the AWS Console, detected by the drift workflow, and reconciled through Terraform.

### Drift introduced

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/Screenshot%202026-10-23%20at%2009.56.37.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/Screenshot%202026-10-23%20at%2009.57.03.png)

### Drift detected

![Drift detected](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/screenshot%2015.png)

### Drift resolved

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/Screenshot%202026-10-23%20at%2010.13.39.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/Screenshot%202026-10-23%20at%2010.15.36.png)

## Failure Testing and Recovery

A unit test is deliberately changed to produce a failure. The CI workflow detects the failure, and the test is restored to confirm that the pipeline can pass again.

### CI failure

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/9b55172bc84fb43d9986702431d073d446fa11d4/screenshots/Screenshot%202026-10-23%20at%2010.20.16.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/9b55172bc84fb43d9986702431d073d446fa11d4/screenshots/Screenshot%202026-10-23%20at%2010.21.14.png)

### CI recovery

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/9b55172bc84fb43d9986702431d073d446fa11d4/screenshots/Screenshot%202026-10-23%20at%2010.20.28.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/9b55172bc84fb43d9986702431d073d446fa11d4/screenshots/Screenshot%202026-10-23%20at%2010.22.19.png)

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
