# Project Atlas — AWS DevOps Project

## Overview

Project Atlas is a hands-on DevOps project demonstrating the development, deployment, monitoring, and management of a serverless application on AWS.

The project integrates GitHub Actions, Terraform, AWS Lambda, AWS IAM OpenID Connect (OIDC), Amazon S3, and Amazon CloudWatch to demonstrate CI/CD automation, Infrastructure as Code (IaC), secure cloud authentication, infrastructure drift detection, and operational testing.

The project was developed using the GitHub web interface and AWS Management Console, demonstrating how a cloud-based DevOps workflow can be implemented without relying on a local command-line environment.

## Objectives

- Automate application testing and infrastructure validation.
- Provision AWS resources using Terraform.
- Configure GitHub Actions to authenticate to AWS through OIDC.
- Store Terraform state remotely in Amazon S3 with state locking.
- Deploy a Python health-check application to AWS Lambda.
- Monitor application activity and errors using CloudWatch.
- Detect and investigate infrastructure drift.
- Test CI failure scenarios and recovery.
- Validate IAM trust restrictions through negative security testing.
- Implement a controlled, confirmation-based infrastructure-destruction workflow.

## Architecture

GitHub Repository → GitHub Actions → GitHub OIDC → AWS IAM → Terraform → AWS Lambda → Amazon CloudWatch

Amazon S3 provides remote Terraform state storage, while S3-native state locking helps coordinate infrastructure operations.

### Technology Stack

| Technology | Purpose |
|---|---|
| GitHub | Source control and repository management |
| GitHub Actions | Continuous integration and infrastructure automation |
| Python | Application development and unit testing |
| AWS IAM and OIDC | Federated authentication and temporary AWS credentials |
| Terraform | Infrastructure as Code |
| Amazon S3 | Remote Terraform state storage |
| AWS Lambda | Serverless application hosting |
| Lambda Function URL | HTTP access to the health-check endpoint |
| Amazon CloudWatch | Logging and error monitoring |

## Repository Structure

```text
.
├── .github/
│   └── workflows/
├── app/
│   ├── handler.py
│   └── test_handler.py
├── infrastructure/
│   ├── main.tf
│   ├── outputs.tf
│   ├── provider.tf
│   ├── variables.tf
│   └── versions.tf
├── screenshots/
└── README.md
```

- `app/` contains the Python Lambda handler and unit tests.
- `.github/workflows/` contains the GitHub Actions automation workflows.
- `infrastructure/` contains the Terraform configuration and backend settings.
- `screenshots/` contains visual evidence of the implementation and test results.

## Workflow Overview

The project separates application validation, deployment, security testing, and infrastructure management into distinct workflows.

| Workflow | Responsibility |
|---|---|
| Continuous integration | Runs Python unit tests and validates Terraform configuration. |
| Deployment | Authenticates to AWS using OIDC and manages infrastructure through Terraform. |
| Drift detection | Generates Terraform plans to identify configuration differences. |
| OIDC security test | Verifies that a workflow without the trusted GitHub Environment cannot assume the deployment role. |
| Infrastructure destruction | Provides a manually triggered, confirmation-gated destruction process. |

## Application Development and Unit Testing

The application is implemented in Python and provides a health-check response through an AWS Lambda handler.

The response includes:

- Application health status.
- Service name.
- Application version.
- UTC timestamp.
- Lambda request ID.

The handler also records structured log events to support troubleshooting and monitoring through CloudWatch.

**Relevant files:** `app/handler.py` and `app/test_handler.py`.

### Application Source Code

![Python Lambda handler implementation](https://github.com/imed3721/project-atlas-devops/blob/c915fe138e4fcbc31d172751fb85b72423a4196f/screenshots/Screenshot%202026-10-23%20at%2007.20.21.png)

![Application response structure](https://github.com/imed3721/project-atlas-devops/blob/c915fe138e4fcbc31d172751fb85b72423a4196f/screenshots/Screenshot%202026-10-23%20at%2007.20.31.png)

![Application logging implementation](https://github.com/imed3721/project-atlas-devops/blob/c915fe138e4fcbc31d172751fb85b72423a4196f/screenshots/Screenshot%202026-10-23%20at%2007.20.40.png)

![Python unit tests](https://github.com/imed3721/project-atlas-devops/blob/c915fe138e4fcbc31d172751fb85b72423a4196f/screenshots/Screenshot%202026-10-23%20at%2007.20.47.png)

## Continuous Integration

GitHub Actions automates application testing and Terraform configuration validation.

This workflow provides an early feedback mechanism for identifying application regressions and infrastructure configuration errors before deployment.

### CI Workflow

![GitHub Actions CI workflow configuration](https://github.com/imed3721/project-atlas-devops/blob/0bee79e836076e4f459e58f1d795b578e8d2cbe3/screenshots/Screenshot%202026-10-23%20at%2007.21.38.png)

![Automated Python test execution](https://github.com/imed3721/project-atlas-devops/blob/0bee79e836076e4f459e58f1d795b578e8d2cbe3/screenshots/Screenshot%202026-10-23%20at%2007.21.49.png)

![CI workflow result](https://github.com/imed3721/project-atlas-devops/blob/0bee79e836076e4f459e58f1d795b578e8d2cbe3/screenshots/Screenshot%202026-10-23%20at%2007.21.56.png)

## Secure GitHub-to-AWS Authentication

GitHub Actions uses OpenID Connect (OIDC) to request temporary AWS credentials rather than relying on long-lived AWS access keys stored in GitHub.

AWS evaluates the GitHub-issued token against the IAM role's trust policy before allowing role assumption. The trust policy includes conditions for the token audience and the permitted repository/environment subject.

The deployment workflow uses the `atlas-dev` GitHub Environment.

### OIDC Configuration

![AWS IAM OIDC provider and role configuration](https://github.com/imed3721/project-atlas-devops/blob/dca7719da5fcbea165ca6c7fe29861f7e4705042/screenshots/Screenshot%202026-10-23%20at%2007.41.13.png)

![IAM trust policy conditions](https://github.com/imed3721/project-atlas-devops/blob/dca7719da5fcbea165ca6c7fe29861f7e4705042/screenshots/Screenshot%202026-10-23%20at%2007.41.22.png)

### OIDC Security-Boundary Testing

A negative security test was implemented to verify that a GitHub Actions workflow without the trusted `atlas-dev` environment could not assume the AWS deployment role.

The test deliberately omitted the environment declaration and attempted to configure AWS credentials through OIDC. AWS rejected the role-assumption attempt with `sts:AssumeRoleWithWebIdentity`, and the workflow treated the rejection as a successful security test.

This provides evidence that the tested workflow context did not satisfy the configured IAM trust conditions. The test validates the environment-specific restriction; it does not independently establish isolation from a separate GitHub repository.

![OIDC security test evidence](https://github.com/imed3721/project-atlas-devops/blob/4083405d6891f0275a631c6d165916e702c3949f/screenshots/Screenshot%202026-10-23%20at%2010.31.21.png)

![OIDC role-assumption test](https://github.com/imed3721/project-atlas-devops/blob/4083405d6891f0275a631c6d165916e702c3949f/screenshots/Screenshot%202026-10-23%20at%2010.33.01.png)

![OIDC security test result](https://github.com/imed3721/project-atlas-devops/blob/4083405d6891f0275a631c6d165916e702c3949f/screenshots/Screenshot%202026-10-23%20at%2010.41.20.png)

## Terraform Infrastructure and Remote State

Terraform defines and manages the AWS infrastructure required by Project Atlas.

The configuration includes:

- An AWS Lambda function.
- A dedicated Lambda execution role.
- Permissions for Lambda logging.
- A CloudWatch log group with configured retention.
- A Lambda Function URL and invocation permissions.
- Application environment variables and deployment settings.

Terraform variables provide reusable configuration for the AWS region, project name, and application version.

### Remote State Management

Terraform state is stored in Amazon S3 so that infrastructure workflows can use a shared remote state file.

The backend configuration enables state encryption and S3-native state locking through `use_lockfile = true`.

Remote state and locking support coordinated infrastructure operations and reduce the risk of conflicting state modifications. S3 bucket versioning can provide an additional recovery mechanism and should be verified separately before being described as an enabled control.

### Terraform State Bucket

![Amazon S3 Terraform state bucket](https://github.com/imed3721/project-atlas-devops/blob/dca7719da5fcbea165ca6c7fe29861f7e4705042/screenshots/Screenshot%202026-10-23%20at%2007.49.28.png)

![Remote Terraform state configuration](https://github.com/imed3721/project-atlas-devops/blob/dca7719da5fcbea165ca6c7fe29861f7e4705042/screenshots/Screenshot%202026-10-23%20at%2007.49.39.png)

### Terraform Configuration

![Terraform provider and version configuration](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.54.43.png)

![Terraform variables](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.54.49.png)

![Terraform resource definitions](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.54.54.png)

![Terraform Lambda configuration](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.55.03.png)

![Terraform outputs and infrastructure settings](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.55.37.png)

## Automated Deployment

The deployment workflow connects GitHub Actions to AWS through OIDC and uses Terraform to manage infrastructure changes.

The workflow validates the Terraform configuration, generates a plan, and applies infrastructure changes through the configured AWS deployment role.

This approach makes infrastructure changes repeatable and provides an execution history through GitHub Actions.

### Deployment Workflow

![GitHub Actions Terraform deployment workflow](https://github.com/imed3721/project-atlas-devops/blob/40c2bf9903d3ccfa8396ef084a3a2f33c706c1f5/screenshots/screenshot%208.png)

### AWS Identity Verification

![AWS identity verification in GitHub Actions](https://github.com/imed3721/project-atlas-devops/blob/40c2bf9903d3ccfa8396ef084a3a2f33c706c1f5/screenshots/screenshot%209.png)

### Terraform Outputs

Terraform outputs expose deployment information such as the Lambda function name, Function URL, and CloudWatch log group name.

![Terraform deployment output](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.11.49.png)

![Terraform resource outputs](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.11.59.png)

![Terraform deployment verification](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.12.07.png)

![Deployed infrastructure details](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.12.15.png)

![Terraform output verification](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.12.24.png)

![Final deployment evidence](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.12.30.png)

## Application Health Check

The deployed Lambda Function URL provides HTTP access to the application's health-check response.

The endpoint returns JSON containing the service status and application metadata, allowing the deployment to be tested through a browser.

The Function URL is configured for public access for demonstration purposes. It is not intended for sensitive workloads or production use without appropriate authentication, access controls, and security review.

### Health-Check Response

![Project Atlas health-check response](https://github.com/imed3721/project-atlas-devops/blob/bcd03361520df044f37848c880105b5118624409/screenshots/Screenshot%2011.png)

## Monitoring and Observability

Amazon CloudWatch provides centralised logging and error monitoring for the Lambda application.

The Terraform configuration defines a dedicated log group with a seven-day retention period. Structured application logs support troubleshooting and help identify health-check activity.

A CloudWatch alarm is also configured to monitor Lambda errors, providing a foundation for operational monitoring.

### CloudWatch Logs

![Project Atlas Lambda logs in CloudWatch](https://github.com/imed3721/project-atlas-devops/blob/bcd03361520df044f37848c880105b5118624409/screenshots/screenshot%2012.png)

### CloudWatch Alarm

![CloudWatch alarm configuration](https://github.com/imed3721/project-atlas-devops/blob/81339602fac5affbb545545a9b137c132e21ee31/screenshots/Screenshot%202026-10-23%20at%2008.59.29.png)

![CloudWatch monitoring settings](https://github.com/imed3721/project-atlas-devops/blob/81339602fac5affbb545545a9b137c132e21ee31/screenshots/Screenshot%202026-10-23%20at%2008.59.10.png)

![CloudWatch alarm verification](https://github.com/imed3721/project-atlas-devops/blob/81339602fac5affbb545545a9b137c132e21ee31/screenshots/Screenshot%202026-10-23%20at%2008.58.17.png)

## Infrastructure Drift Detection

Infrastructure drift occurs when live AWS resources differ from the configuration managed by Terraform.

The drift-detection workflow initialises Terraform, validates the configuration, and generates a plan to identify observable differences between the declared and live infrastructure.

For this demonstration, a manual change was introduced through the AWS Management Console. The workflow was then used to identify the discrepancy and document the subsequent reconciliation.

Terraform can detect only differences that are observable through the configured provider and resources; it does not automatically detect every possible change across an AWS account.

### Drift Introduced

![Manual infrastructure change in AWS](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/Screenshot%202026-10-23%20at%2009.56.37.png)

![Changed AWS resource configuration](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/Screenshot%202026-10-23%20at%2009.57.03.png)

### Drift Detected

![Terraform drift detection workflow result](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/screenshot%2015.png)

### Drift Reconciliation

![Infrastructure reconciliation evidence](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/Screenshot%202026-10-23%20at%2010.13.39.png)

![Post-reconciliation verification](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/Screenshot%202026-10-23%20at%2010.15.36.png)

## Failure Testing and Recovery

Failure testing was used to evaluate how the CI workflow responds to an intentional application-test regression.

A unit test was deliberately modified to cause a failure. GitHub Actions detected the failing test, after which the test was restored and the workflow rerun to demonstrate recovery.

This exercise demonstrates the role of automated testing in identifying regressions before changes progress through the delivery workflow.

### CI Failure

![Intentional unit-test failure](https://github.com/imed3721/project-atlas-devops/blob/9b55172bc84fb43d9986702431d073d446fa11d4/screenshots/Screenshot%202026-10-23%20at%2010.20.16.png)

![CI workflow detecting the test failure](https://github.com/imed3721/project-atlas-devops/blob/9b55172bc84fb43d9986702431d073d446fa11d4/screenshots/Screenshot%202026-10-23%20at%2010.21.14.png)

### CI Recovery

![Recovery after restoring the unit test](https://github.com/imed3721/project-atlas-devops/blob/9b55172bc84fb43d9986702431d073d446fa11d4/screenshots/Screenshot%202026-10-23%20at%2010.20.28.png)

![Successful CI rerun](https://github.com/imed3721/project-atlas-devops/blob/9b55172bc84fb43d9986702431d073d446fa11d4/screenshots/Screenshot%202026-10-23%20at%2010.22.19.png)

## Controlled Infrastructure Destruction

A dedicated GitHub Actions workflow was created to support manual Terraform infrastructure destruction.

The workflow includes:

- Manual execution through `workflow_dispatch`.
- A confirmation input that must match `DESTROY`.
- OIDC-based AWS authentication.
- Terraform initialisation and configuration validation.
- Generation of a saved destroy plan.
- A separate step to apply the saved plan.

These safeguards help reduce the risk of accidental infrastructure removal and make destructive operations more deliberate.

### Destruction Workflow Evidence

![Infrastructure destruction workflow configuration](https://github.com/imed3721/project-atlas-devops/blob/79f81a47df1313ba1d5603d41c9217d8ac155903/screenshots/Screenshot%202026-10-23%20at%2010.54.32.png)

![Destroy workflow confirmation settings](https://github.com/imed3721/project-atlas-devops/blob/79f81a47df1313ba1d5603d41c9217d8ac155903/screenshots/Screenshot%202026-10-23%20at%2010.54.35.png)

![Terraform destroy plan](https://github.com/imed3721/project-atlas-devops/blob/79f81a47df1313ba1d5603d41c9217d8ac155903/screenshots/Screenshot%202026-10-23%20at%2010.54.48.png)

![Destroy workflow execution](https://github.com/imed3721/project-atlas-devops/blob/79f81a47df1313ba1d5603d41c9217d8ac155903/screenshots/Screenshot%202026-10-23%20at%2010.54.53.png)

![Destroy workflow result](https://github.com/imed3721/project-atlas-devops/blob/79f81a47df1313ba1d5603d41c9217d8ac155903/screenshots/Screenshot%202026-10-23%20at%2010.54.58.png)

### Validation Status

The initial destroy run successfully removed several resources, including the Lambda Function URL, public invocation permissions, Lambda function, and CloudWatch log group. However, deletion of the Lambda execution role failed because the deployment role lacked the required `iam:ListInstanceProfilesForRole` permission.

The workflow therefore remains partially validated. The IAM permission issue must be resolved, and a subsequent run must verify that the remaining cleanup completes successfully.

Terraform state should be retained until the cleanup outcome has been verified and any required recovery or reconciliation is complete.

## Security and Future Improvements

The project demonstrates OIDC-based authentication, IAM trust-policy restrictions, resource-scoped permissions, and controlled infrastructure operations. Further improvements could strengthen its security and operational maturity.

Planned improvements include:

- **IAM least privilege:** Continue refining permissions and restrict resource access wherever AWS supports resource-level controls.
- **GitHub Actions security:** Pin third-party actions to verified commit SHAs and review updates.
- **Deployment approvals:** Introduce approval requirements for production infrastructure changes.
- **Endpoint security:** Review authentication and access restrictions before using a public endpoint for sensitive workloads.
- **Monitoring:** Add latency, availability, and application-level metrics.
- **State recovery:** Document recovery procedures for Terraform state and partially completed operations.
- **Destructive workflow validation:** Resolve the outstanding IAM permission issue and verify end-to-end cleanup.
- **Operational documentation:** Document deployment, drift investigation, troubleshooting, and recovery procedures.

## Skills Demonstrated

- GitHub repository and branch management.
- Python application development and unit testing.
- GitHub Actions CI/CD automation.
- AWS IAM and OpenID Connect authentication.
- IAM trust-policy configuration and negative security testing.
- Terraform Infrastructure as Code.
- Amazon S3 remote state and state locking.
- AWS Lambda deployment and health checks.
- Amazon CloudWatch logging and error monitoring.
- Infrastructure drift detection and reconciliation.
- CI failure testing and recovery.
- Controlled infrastructure destruction.
- IAM permission troubleshooting.
- Technical documentation and project reporting.

## Cost Awareness

AWS charges may apply depending on resource usage, region, and account pricing. Lambda, CloudWatch, S3, and other AWS services may incur costs even in small demonstration environments.

AWS Budgets notifications can help identify unexpected spending, but budget alerts do not enforce a hard spending limit.

Resources that are no longer required should be removed carefully. Always review a Terraform destroy plan before applying it, and preserve Terraform state until resource cleanup and any required recovery have been verified.

## Conclusion

Project Atlas demonstrates a practical DevOps workflow spanning application testing, secure cloud authentication, Infrastructure as Code, automated deployment, monitoring, drift detection, and failure recovery.

By documenting both successful tests and outstanding issues, the project reflects the importance of security, observability, controlled change, and continuous improvement in cloud engineering.
