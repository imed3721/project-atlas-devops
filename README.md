
# Project Atlas — AWS DevOps Project

## Overview

Project Atlas demonstrates an end-to-end, browser-based DevOps workflow using GitHub Actions, Terraform, AWS Lambda, AWS IAM OpenID Connect (OIDC), Amazon S3, and Amazon CloudWatch.

The project focuses on automating application testing and infrastructure deployment while exploring cloud security, remote state management, monitoring, infrastructure drift detection, failure testing, and controlled infrastructure destruction.

The project was built using GitHub's web interface and AWS management console, demonstrating how cloud infrastructure and CI/CD workflows can be configured and managed without relying on a local command-line environment.

## Project Objectives

- Automate Python unit testing through GitHub Actions.
- Define AWS infrastructure using Terraform.
- Authenticate GitHub Actions to AWS using OIDC and temporary credentials.
- Store Terraform state remotely in Amazon S3.
- Deploy a Python health-check application to AWS Lambda.
- Monitor application activity through Amazon CloudWatch.
- Detect infrastructure drift using Terraform plans.
- Test CI failure scenarios and recovery.
- Validate IAM trust restrictions with a negative OIDC security test.
- Implement a confirmation-gated infrastructure-destruction workflow.

## Architecture

GitHub repository → GitHub Actions → GitHub OIDC → AWS IAM → Terraform → AWS Lambda → Amazon CloudWatch

Terraform state is stored remotely in Amazon S3, with S3-native state locking configured through Terraform's `use_lockfile` backend option.

### Technology Stack

| Technology | Purpose |
|---|---|
| GitHub | Source control and repository management |
| GitHub Actions | CI/CD automation and infrastructure workflows |
| Python | Application logic and unit tests |
| AWS IAM OIDC | Short-lived AWS authentication for GitHub Actions |
| Terraform | Infrastructure as Code |
| Amazon S3 | Remote Terraform state storage |
| AWS Lambda | Serverless application hosting |
| Lambda Function URL | HTTP access to the health-check endpoint |
| Amazon CloudWatch | Application logs and error monitoring |

## Repository Structure

The main application and infrastructure files are organised as follows:

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
- `.github/workflows/` contains GitHub Actions workflows for CI, deployment, drift detection, security testing, and infrastructure management, where implemented.
- `infrastructure/` contains the Terraform configuration for AWS resources and the remote backend.
- `screenshots/` contains visual evidence of configuration, workflow runs, and AWS resources.

## Workflow Summary

The project uses separate workflows for different stages of the DevOps lifecycle.

| Workflow | Purpose |
|---|---|
| Continuous integration | Runs Python unit tests and validates Terraform configuration. |
| Deployment | Authenticates to AWS using OIDC and manages infrastructure through Terraform. |
| Drift detection | Generates a Terraform plan to identify differences between declared and live infrastructure. |
| OIDC security-boundary test | Checks that a workflow without the trusted GitHub Environment cannot assume the deployment role. |
| Infrastructure destruction | Provides a manually triggered, confirmation-gated Terraform destroy process. |

The CI workflow checks application and configuration changes, while deployment and infrastructure-management workflows handle changes to AWS resources.

## Application and Unit Tests

The Python application exposes a health-check response through an AWS Lambda handler.

The handler returns a JSON response containing:

- Application health status.
- Service name.
- Application version.
- UTC timestamp.
- AWS Lambda request ID.

Structured logging records health-check activity in a format suitable for CloudWatch.

Relevant files:

- `app/handler.py`
- `app/test_handler.py`

### Application source code

![Python Lambda handler implementation](https://github.com/imed3721/project-atlas-devops/blob/c915fe138e4fcbc31d172751fb85b72423a4196f/screenshots/Screenshot%202026-10-23%20at%2007.20.21.png)

![Application response structure](https://github.com/imed3721/project-atlas-devops/blob/c915fe138e4fcbc31d172751fb85b72423a4196f/screenshots/Screenshot%202026-10-23%20at%2007.20.31.png)

![Application logging implementation](https://github.com/imed3721/project-atlas-devops/blob/c915fe138e4fcbc31d172751fb85b72423a4196f/screenshots/Screenshot%202026-10-23%20at%2007.20.40.png)

![Python unit tests](https://github.com/imed3721/project-atlas-devops/blob/c915fe138e4fcbc31d172751fb85b72423a4196f/screenshots/Screenshot%202026-10-23%20at%2007.20.47.png)

## Continuous Integration

GitHub Actions provides automated checks for application and infrastructure changes.

The CI workflow runs Python unit tests and validates the Terraform configuration. This helps identify regressions and configuration errors before infrastructure changes are deployed.

### CI workflow

![GitHub Actions CI workflow configuration](https://github.com/imed3721/project-atlas-devops/blob/0bee79e836076e4f459e58f1d795b578e8d2cbe3/screenshots/Screenshot%202026-10-23%20at%2007.21.38.png)

![Automated Python test execution](https://github.com/imed3721/project-atlas-devops/blob/0bee79e836076e4f459e58f1d795b578e8d2cbe3/screenshots/Screenshot%202026-10-23%20at%2007.21.49.png)

![CI workflow result](https://github.com/imed3721/project-atlas-devops/blob/0bee79e836076e4f459e58f1d795b578e8d2cbe3/screenshots/Screenshot%202026-10-23%20at%2007.21.56.png)

## Secure GitHub-to-AWS Authentication

GitHub Actions authenticates to AWS using OpenID Connect rather than storing long-lived AWS access keys in GitHub repository secrets.

The workflow requests an OIDC token, which AWS STS uses to evaluate the IAM role's trust policy. When the token satisfies the configured conditions, AWS issues temporary credentials to the workflow.

The trust policy restricts role assumption using GitHub OIDC claims, including the audience and the trusted repository/environment subject.

The project uses the `atlas-dev` GitHub Environment for the deployment workflow.

### OIDC configuration

![AWS IAM OIDC provider and role configuration](https://github.com/imed3721/project-atlas-devops/blob/dca7719da5fcbea165ca6c7fe29861f7e4705042/screenshots/Screenshot%202026-10-23%20at%2007.41.13.png)

![IAM trust policy conditions](https://github.com/imed3721/project-atlas-devops/blob/dca7719da5fcbea165ca6c7fe29861f7e4705042/screenshots/Screenshot%202026-10-23%20at%2007.41.22.png)

### OIDC security-boundary testing

A negative security test was implemented to check that the deployment role could not be assumed by a GitHub Actions workflow that deliberately omitted the trusted `atlas-dev` environment.

The test attempted to configure AWS credentials using OIDC without declaring the GitHub Environment. AWS rejected the role assumption with `sts:AssumeRoleWithWebIdentity`, and the workflow evaluated the rejection as a successful security test.

This demonstrates that the tested workflow context did not satisfy the configured IAM trust conditions.

The test validates the environment-specific trust restriction. It does not independently demonstrate isolation from a separate GitHub repository.

Key security controls include:

- Temporary AWS credentials obtained through OIDC.
- No long-lived AWS access keys required by the workflow.
- IAM trust conditions that restrict role assumption.
- A negative test that verifies rejection of an untrusted workflow context.

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/4083405d6891f0275a631c6d165916e702c3949f/screenshots/Screenshot%202026-10-23%20at%2010.31.21.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/4083405d6891f0275a631c6d165916e702c3949f/screenshots/Screenshot%202026-10-23%20at%2010.33.01.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/4083405d6891f0275a631c6d165916e702c3949f/screenshots/Screenshot%202026-10-23%20at%2010.41.20.png)

## Terraform Infrastructure and Remote State

Terraform defines the AWS resources required to run Project Atlas.

The infrastructure configuration includes:

- An AWS Lambda function.
- A dedicated Lambda execution role.
- Permissions for Lambda to write logs.
- A CloudWatch log group with configured retention.
- A Lambda Function URL and its invocation permissions.
- Application environment variables and deployment settings.

The configuration uses reusable variables for the AWS region, project name, and application version.

### Terraform state management

Terraform state is stored remotely in Amazon S3 rather than relying solely on a local state file.

The backend is configured with:

- An S3 state bucket.
- A dedicated state key for the development environment.
- State encryption.
- S3-native lockfile support using `use_lockfile = true`.

Remote state allows Terraform workflows to share the same infrastructure state. Locking helps prevent concurrent operations from modifying the state simultaneously.

Bucket versioning is a useful additional recovery control and should be documented as enabled only after it has been verified in the AWS console.

### Terraform state bucket

![Amazon S3 Terraform state bucket](https://github.com/imed3721/project-atlas-devops/blob/dca7719da5fcbea165ca6c7fe29861f7e4705042/screenshots/Screenshot%202026-10-23%20at%2007.49.28.png)

![Remote Terraform state configuration](https://github.com/imed3721/project-atlas-devops/blob/dca7719da5fcbea165ca6c7fe29861f7e4705042/screenshots/Screenshot%202026-10-23%20at%2007.49.39.png)

### Terraform configuration

![Terraform provider and version configuration](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.54.43.png)

![Terraform variables](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.54.49.png)

![Terraform resource definitions](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.54.54.png)

![Terraform Lambda configuration](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.55.03.png)

![Terraform outputs and infrastructure settings](https://github.com/imed3721/project-atlas-devops/blob/310e37166b530b5085530117b966c58bf7ab4e89/screenshots/Screenshot%202026-10-23%20at%2007.55.37.png)

## Automated Deployment

The deployment workflow connects GitHub Actions to AWS through OIDC and uses Terraform to manage infrastructure.

The workflow validates the Terraform configuration, generates a plan, and applies infrastructure changes through the configured AWS deployment role.

This separates infrastructure definition from execution and makes deployment activity visible through GitHub Actions logs.

### Deployment workflow

![GitHub Actions Terraform deployment workflow](https://github.com/imed3721/project-atlas-devops/blob/40c2bf9903d3ccfa8396ef084a3a2f33c706c1f5/screenshots/screenshot%208.png)

### AWS identity verification

![AWS identity verification in GitHub Actions](https://github.com/imed3721/project-atlas-devops/blob/40c2bf9903d3ccfa8396ef084a3a2f33c706c1f5/screenshots/screenshot%209.png)

### Terraform outputs

Terraform outputs expose useful deployment information, including the Lambda function name, Function URL, and CloudWatch log group name.

![Terraform deployment output](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.11.49.png)

![Terraform resource outputs](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.11.59.png)

![Terraform deployment verification](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.12.07.png)

![Deployed infrastructure details](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.12.15.png)

![Terraform output verification](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.12.24.png)

![Final deployment evidence](https://github.com/imed3721/project-atlas-devops/blob/e6d5f2441a893900a085ee8aa0cb4bd5b22d080e/screenshots/Screenshot%202026-10-23%20at%2008.12.30.png)

## Application Health Check

The deployed Lambda Function URL provides an HTTP endpoint for checking application health.

The handler returns a JSON response indicating the service's health, along with version and request metadata. This provides a simple way to verify that the deployed application can be invoked and returns the expected response.

The Function URL is configured for public access in this demonstration. It is intended for a non-sensitive test application and should not be treated as a production-ready public endpoint without appropriate access controls and further security review.

### Health-check response

![Project Atlas health-check response](https://github.com/imed3721/project-atlas-devops/blob/bcd03361520df044f37848c880105b5118624409/screenshots/Screenshot%2011.png)

## Monitoring and Observability

Amazon CloudWatch provides centralised logging for the Lambda application and supports monitoring of function errors.

The Terraform configuration defines a dedicated log group with a retention period of seven days. The application writes structured health-check events that can be inspected during troubleshooting.

A CloudWatch alarm is also configured to monitor Lambda errors, providing a foundation for identifying application failures.

### CloudWatch logs

![Project Atlas Lambda logs in CloudWatch](https://github.com/imed3721/project-atlas-devops/blob/bcd03361520df044f37848c880105b5118624409/screenshots/screenshot%2012.png)

### CloudWatch alarm

![CloudWatch alarm configuration](https://github.com/imed3721/project-atlas-devops/blob/81339602fac5affbb545545a9b137c132e21ee31/screenshots/Screenshot%202026-10-23%20at%2008.59.29.png)

![CloudWatch monitoring settings](https://github.com/imed3721/project-atlas-devops/blob/81339602fac5affbb545545a9b137c132e21ee31/screenshots/Screenshot%202026-10-23%20at%2008.59.10.png)

![CloudWatch alarm verification](https://github.com/imed3721/project-atlas-devops/blob/81339602fac5affbb545545a9b137c132e21ee31/screenshots/Screenshot%202026-10-23%20at%2008.58.17.png)

## Infrastructure Drift Detection

Infrastructure drift occurs when live cloud resources differ from the configuration managed by Terraform.

The drift-detection workflow initialises Terraform, validates the configuration, and generates a plan to compare the declared configuration with the observed infrastructure.

For the demonstration, a manual change was introduced through the AWS Console. The workflow was then used to identify the discrepancy and verify the subsequent reconciliation.

Terraform drift detection is limited to differences that the provider and resource configuration can observe. It should not be assumed to detect every possible change to an AWS account or resource.

### Drift introduced

![Manual infrastructure change in AWS](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/Screenshot%202026-10-23%20at%2009.56.37.png)

![Changed AWS resource configuration](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/Screenshot%202026-10-23%20at%2009.57.03.png)

### Drift detected

![Terraform drift detection workflow result](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/screenshot%2015.png)

### Drift reconciliation

![Infrastructure reconciliation evidence](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/Screenshot%202026-10-23%20at%2010.13.39.png)

![Post-reconciliation verification](https://github.com/imed3721/project-atlas-devops/blob/e53536777abe637fbafcc8f962f5438aa691ba49/screenshots/Screenshot%202026-10-23%20at%2010.15.36.png)

## Failure Testing and Recovery

Failure testing demonstrates how automated checks respond to an intentional regression.

A unit test was deliberately modified to introduce a failure. The CI workflow detected the failed test, preventing the change from passing the automated checks. The test was then restored and the workflow rerun to demonstrate recovery.

This validates the importance of automated testing as an early safeguard against application regressions.

### CI failure

![Intentional unit-test failure](https://github.com/imed3721/project-atlas-devops/blob/9b55172bc84fb43d9986702431d073d446fa11d4/screenshots/Screenshot%202026-10-23%20at%2010.20.16.png)

![CI workflow detecting the test failure](https://github.com/imed3721/project-atlas-devops/blob/9b55172bc84fb43d9986702431d073d446fa11d4/screenshots/Screenshot%202026-10-23%20at%2010.21.14.png)

### CI recovery

![Recovery after restoring the unit test](https://github.com/imed3721/project-atlas-devops/blob/9b55172bc84fb43d9986702431d073d446fa11d4/screenshots/Screenshot%202026-10-23%20at%2010.20.28.png)

![Successful CI rerun](https://github.com/imed3721/project-atlas-devops/blob/9b55172bc84fb43d9986702431d073d446fa11d4/screenshots/Screenshot%202026-10-23%20at%2010.22.19.png)

## Controlled Infrastructure Destruction

Infrastructure destruction is a separate operation from normal deployment and requires additional safeguards.

A dedicated GitHub Actions workflow was created to support manual Terraform destruction. It requires a confirmation input matching `DESTROY`, authenticates to AWS through OIDC, validates the Terraform configuration, generates a saved destroy plan, and applies that plan in a subsequent step.

The confirmation requirement reduces the risk of accidental destruction, while the saved plan provides a defined set of changes for the apply step.

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/79f81a47df1313ba1d5603d41c9217d8ac155903/screenshots/Screenshot%202026-10-23%20at%2010.54.32.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/79f81a47df1313ba1d5603d41c9217d8ac155903/screenshots/Screenshot%202026-10-23%20at%2010.54.35.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/79f81a47df1313ba1d5603d41c9217d8ac155903/screenshots/Screenshot%202026-10-23%20at%2010.54.48.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/79f81a47df1313ba1d5603d41c9217d8ac155903/screenshots/Screenshot%202026-10-23%20at%2010.54.53.png)

![Image Alt](https://github.com/imed3721/project-atlas-devops/blob/79f81a47df1313ba1d5603d41c9217d8ac155903/screenshots/Screenshot%202026-10-23%20at%2010.54.58.png)

### Validation status

The initial destroy run successfully removed several resources, including the Lambda Function URL, public invocation permissions, Lambda function, and CloudWatch log group. However, deletion of the Lambda execution role failed because the deployment role lacked permission for `iam:ListInstanceProfilesForRole`.

The workflow therefore still requires end-to-end validation. The missing IAM permission must be addressed with an appropriately scoped policy, and the workflow must be rerun to verify successful cleanup.

Until that verification is complete, the infrastructure-destruction process should be considered **partially tested rather than fully successful**.

Terraform state should be preserved until cleanup is verified and any necessary recovery or reconciliation has been completed.

## Security and Future Improvements

The project demonstrates several security controls, including OIDC-based authentication, IAM role trust conditions, and resource-scoped permissions. Further work would strengthen the project for more demanding or production-like environments.

Potential improvements include:

- **IAM least privilege:** Continue reviewing permissions and reduce broad resource scopes wherever AWS supports resource-level restrictions.
- **GitHub Actions supply-chain security:** Pin third-party actions to verified commit SHAs and review action updates.
- **Deployment approvals:** Require environment approval before applying changes to production infrastructure.
- **Endpoint security:** Add authentication or suitable access restrictions before exposing a sensitive application through a public endpoint.
- **Monitoring:** Introduce latency, availability, and application-level metrics, alongside suitable alarm thresholds.
- **State recovery:** Document restoration procedures, state-version recovery, and recovery from partially completed Terraform operations.
- **Destructive workflow safeguards:** Complete testing of the destroy workflow and verify that IAM permissions are limited to the required resources.
- **Operational documentation:** Document deployment, drift investigation, failure recovery, and cleanup procedures.

## Skills Demonstrated

- GitHub repository and branch management.
- Python application development and unit testing.
- GitHub Actions CI/CD workflow configuration.
- AWS IAM role configuration and OpenID Connect authentication.
- IAM trust-policy restrictions and negative security testing.
- Terraform Infrastructure as Code.
- Amazon S3 remote state and state locking.
- AWS Lambda deployment and HTTP health checks.
- Amazon CloudWatch logging and error monitoring.
- Infrastructure drift detection and reconciliation.
- Failure testing and CI recovery.
- Confirmation-gated infrastructure destruction.
- IAM permission troubleshooting.
- Technical documentation and evidence-based project reporting.

## Cost Awareness

AWS charges may apply depending on resource usage, region, and account pricing. Lambda, CloudWatch, S3, and other services may incur costs even in small demonstration environments.

AWS Budgets notifications can help identify unexpected spending, but budget alerts do not impose a hard spending limit.

Resources that are no longer required should be removed carefully. Before destroying infrastructure, review the Terraform plan and confirm that the correct resources are targeted. Preserve Terraform state until resource cleanup and any necessary recovery have been verified.

## Conclusion

Project Atlas brings together application development, automated testing, cloud authentication, Infrastructure as Code, deployment, monitoring, and operational testing in one documented DevOps project.

The project also explores failure scenarios and security boundaries rather than focusing exclusively on a successful deployment. The remaining priority is to complete end-to-end validation of the infrastructure-destruction workflow and continue refining IAM permissions and operational safeguards.
