# Intro to DevOps — FruitAPI

This repository contains the course homework application for the Intro to DevOps course.

FruitAPI is a small REST API for managing fruits. The application is intentionally simple so the focus stays on DevOps practices: testing, Docker, CI/CD, infrastructure as code, AWS deployment, logging, high availability, and release automation.

## Application features

The API supports:

- `GET /health` — health check endpoint
- `GET /fruits` — list all fruits
- `GET /fruits?in_season=true|false` — filter fruits by season
- `GET /fruits/cheapest` — get the cheapest fruit
- `POST /fruits` — create a fruit
- `GET /fruits/{id}` — get one fruit
- `PUT /fruits/{id}` — update a fruit
- `DELETE /fruits/{id}` — delete a fruit

## Tech stack

- Python
- FastAPI
- SQLAlchemy
- MySQL
- Pytest
- Docker / Docker Compose
- GitHub Actions
- GitHub Container Registry
- Terraform
- AWS ECS Fargate
- AWS RDS MySQL
- AWS Application Load Balancer
- AWS CloudWatch Logs
- AWS Secrets Manager

## Project structure

```text
app/
  api.py          # FastAPI routes
  config.py       # Environment-based configuration
  database.py     # SQLAlchemy database setup
  models.py       # SQLAlchemy and Pydantic models
  store.py        # Fruit data access logic

tests/
  unit/           # Unit tests
  integration/    # HTTP integration tests

infra/
  main.tf         # AWS infrastructure
  variables.tf    # Terraform variables
  outputs.tf      # Terraform outputs
  terraform.tfvars.example

.github/workflows/
  pr-tests.yml    # Pull request unit-test workflow
  main.yml        # Main CI/CD workflow
```

## Branching strategy

This project uses GitHub Flow.

- `main` is the stable branch.
- All changes are developed in feature branches.
- Feature branches are merged into `main` through Pull Requests.
- Pull Requests must pass the unit-test workflow before merging.
- After a Pull Request is merged, the feature branch is deleted.
- Before starting new work, local `main` is updated with `git pull origin main`.

## Local setup

Create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the API locally:

```powershell
python -m uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
```

## Running tests

Run unit tests:

```powershell
python -m pytest tests/unit
```

Run integration tests against a running API:

```powershell
python -m pytest tests/integration
```

Run all tests:

```powershell
python -m pytest
```

## Running with Docker Compose

Build and start the app with MySQL:

```powershell
docker compose up --build
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Stop the containers:

```powershell
docker compose down
```

Delete local MySQL data if needed:

```powershell
docker compose down -v
```

## Docker image

The main pipeline builds and pushes the Docker image to GitHub Container Registry:

```text
ghcr.io/togoevidato/intro-to-devops-starter:latest
```

## CI/CD

GitHub Actions workflows:

### Pull Request workflow

Runs on Pull Requests.

It:

- installs dependencies
- runs unit tests
- helps prevent broken code from being merged into `main`

### Main CI/CD workflow

Runs on push to `main`.

It:

- runs unit tests
- builds the Docker image
- starts Docker Compose
- runs integration tests
- pushes the Docker image to GitHub Container Registry
- triggers a new AWS ECS deployment
- waits for the ECS service to become stable
- verifies the ECS deployment

Required GitHub Actions secrets:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

Required GitHub Actions variables:

```text
AWS_REGION
ECS_CLUSTER_NAME
ECS_SERVICE_NAME
ALB_URL
```

## Infrastructure

Terraform code is located in:

```text
infra/
```

The infrastructure includes:

- VPC
- public and private subnets
- ECS Fargate cluster
- ECS service with multiple replicas
- RDS MySQL database
- Application Load Balancer
- CloudWatch log group
- Secrets Manager secret for database password
- IAM role for ECS task execution
- Security groups for ALB, ECS, and RDS

Create a local Terraform variables file:

```powershell
copy infra\terraform.tfvars.example infra\terraform.tfvars
```

Edit `infra/terraform.tfvars` and provide real values.

Initialize Terraform:

```powershell
cd infra
terraform init
```

Format and validate:

```powershell
terraform fmt
terraform validate
```

Plan infrastructure changes:

```powershell
terraform plan
```

Apply infrastructure changes:

```powershell
terraform apply
```

Destroy infrastructure after review/grading if needed:

```powershell
terraform destroy
```

## Deployment verification

Get the ALB URL:

```powershell
cd infra
terraform output -raw alb_url
```

Check health:

```powershell
curl http://YOUR_ALB_URL/health
```

Expected response:

```json
{"status":"ok"}
```

Check fruits:

```powershell
curl http://YOUR_ALB_URL/fruits
```

Verify ECS service:

```powershell
aws ecs describe-services --cluster fruitapi-cluster --services fruitapi-service --region eu-central-1
```

Expected state:

```text
desiredCount = 2
runningCount = 2
```

Verify ALB target health:

```powershell
$tgArn = terraform output -raw target_group_arn
aws elbv2 describe-target-health --target-group-arn $tgArn --region eu-central-1
```

Expected target state:

```text
healthy
```

## Logs

Application logs are collected in CloudWatch Logs.

Region:

```text
eu-central-1
```

Log group:

```text
/ecs/fruitapi
```

## Security notes

- Secrets are not committed to the repository.
- `terraform.tfvars`, `.env`, Terraform state files, and virtual environment files are ignored by Git.
- Database password is passed to ECS through AWS Secrets Manager.
- RDS is not publicly accessible.
- ALB access is restricted by security group configuration.
