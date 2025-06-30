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


## Seed Data
Run:
```bash
TABLE=<dynamoName> npx ts-node scripts/seed-dev-data.ts

```

## Local API
```bash
sam local start-api -t infra/trainer-svc/template.yaml
```
