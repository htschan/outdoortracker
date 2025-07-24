# GitHub Actions CI/CD Setup

This document provides information about the Continuous Integration and Continuous Deployment (CI/CD) setup for the Outdoor Tracker project using GitHub Actions.

## Workflows

The project contains three main workflows:

### 1. Build and Test (`build-and-test.yml`)

This workflow runs on:
- Every push to any branch
- Pull requests targeting the main branch

It performs the following jobs:
- **Backend Tests**: Runs Python tests using pytest with coverage reports
- **Frontend Tests**: Runs linting, unit tests, and builds the frontend
- **Docker Build**: Builds Docker images (only on main branch or PRs to main)

### 2. Deploy (`deploy.yml`)

This workflow runs on:
- Pushes to the main branch
- Manual trigger via GitHub interface

It performs the following tasks:
- Builds and pushes Docker images to Docker Hub
- Deploys the application (placeholder for actual deployment steps)

### 3. Security Scan (`security-scan.yml`)

This workflow runs on:
- Pushes to the main branch
- Pull requests targeting the main branch
- Weekly schedule (Mondays at 8:00 UTC)

It performs security checks including:
- Bandit for Python code scanning
- Safety for Python dependencies
- npm audit for JavaScript dependencies
- GitHub CodeQL analysis

## Required Secrets

To use these workflows, you need to set up the following secrets in your GitHub repository:

1. `MYREG_URL`: Your private registry URL (e.g., registry.example.com)
2. `MYREG_USERNAME`: Your registry username
3. `MYREG_TOKEN`: Your registry authentication token or password

## Setting Up Secrets

1. Go to your repository on GitHub
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Add the required secrets mentioned above

## Customizing Workflows

### Deployment

The deployment workflow currently contains a placeholder. To implement actual deployment:

1. Edit the `.github/workflows/deploy.yml` file
2. Update the "Deploy application" step with your actual deployment commands
3. Add any necessary secrets for deployment (SSH keys, etc.)

### Test Environment

The test environment variables in the build workflow can be customized:

1. Edit the `.github/workflows/build-and-test.yml` file
2. Update the environment variables in the "Run tests" step

## Monitoring Workflows

You can monitor the execution of these workflows in the "Actions" tab of your GitHub repository.

## Troubleshooting

If a workflow fails, you can:

1. Click on the failed workflow in the Actions tab
2. Examine the logs of the failed job
3. Make necessary changes to your code or workflow files
4. Push the changes to trigger the workflow again
