# Certification & Training Tracking System (CTTS)

## Prerequisites
- Node 18
- AWS CLI v2
- AWS CDK v2
- AWS SAM CLI

## Quick Start
```bash
npm install -w services/trainer
npm install -w services/admin
```

## UI Repository
The frontend application is now maintained in a separate repository.
Clone `ctts-ui` and follow its README for setup instructions.

## Seed Data
Run:
```bash
CLUSTER_ARN=<clusterArn> SECRET_ARN=<secretArn> npx ts-node scripts/seed-dev-data.ts
```

## Local API
```bash
sam local start-api -t infra/trainer-svc/template.yaml
```
