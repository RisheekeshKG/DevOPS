# CI/CD Pipeline Documentation

## Overview

This project uses **GitLab CI/CD** for automated testing, building, and deployment.

### Pipeline Stages

```
Push Code → [Lint] → [Test] → [Build Docker] → [Push to Registry] → [Deploy]
```

---

## 🚀 Quick Setup Guide

### Step 1: Push Code to GitLab

```bash
git init
git remote add origin <your-gitlab-repo-url>
git add .
git commit -m "Initial commit with CI/CD"
git push -u origin main
```

### Step 2: Configure GitLab CI/CD Variables

Go to your GitLab project:
**Settings → CI/CD → Variables**

Add these **protected & masked** variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DOCKER_REGISTRY_URL` | GitLab registry URL | `registry.gitlab.com` |
| `DEPLOY_SERVER_HOST` | Server IP/hostname | `192.168.1.100` or `example.com` |
| `DEPLOY_SERVER_USER` | SSH username | `ubuntu` or `root` |
| `DEPLOY_SERVER_KEY` | SSH private key | Paste your private key |
| `DEPLOY_PATH` | Path to docker-compose on server | `/opt/patient-monitoring` |

### Step 3: Generate SSH Key for Deployment

**On your local machine:**

```bash
# Generate SSH key pair
ssh-keygen -t ed25519 -C "gitlab-ci@patient-monitoring" -f ~/.ssh/gitlab-ci-deploy

# Copy public key to server
ssh-copy-id -i ~/.ssh/gitlab-ci-deploy.pub user@your-server-ip

# View private key (copy this to GitLab CI/CD variable)
cat ~/.ssh/gitlab-ci-deploy
```

**In GitLab:**
- Go to **Settings → CI/CD → Variables**
- Add `DEPLOY_SERVER_KEY` with the private key content
- Check **"Mask variable"** and **"Protect variable"**

---

## 📂 Files Created

### 1. `.gitlab-ci.yml` (root)
Main CI/CD pipeline configuration
- **Stages**: lint → test → build → push → deploy
- **Runs on**: Every push and merge request

### 2. `tests/` (new folder)
Unit tests for all Python modules
- `test_sensor_data_gen.py` - Sensor data generation tests
- `test_kafka_prod_cons.py` - Risk labeling tests
- `test_influxDB.py` - InfluxDB writer tests
- `test_main_workflow.py` - Integration tests

### 3. `requirements-dev.txt`
Development dependencies (testing + linting tools)

### 4. `pytest.ini`
Pytest configuration for test discovery

### 5. `.dockerignore`
Optimizes Docker build by excluding unnecessary files

### 6. `deploy.sh`
Manual deployment script for server (alternative to CI/CD)

---

## 🔧 Pipeline Configuration

### CI Pipeline (Always Runs)

| Stage | Job | Description |
|-------|-----|-------------|
| **lint** | `lint` | Checks code quality with flake8 & pylint |
| **test** | `test` | Runs unit tests with pytest, generates coverage report |
| **build** | `build:docker` | Builds Docker image and validates it |

### CD Pipeline (Main Branch Only)

| Stage | Job | Description |
|-------|-----|-------------|
| **push** | `push:registry` | Pushes image to GitLab Container Registry |
| **deploy** | `deploy:production` | Deploys to production server via SSH |

---

## 🎯 How It Works

### On Every Push (Any Branch)
```
1. ✅ Lint code (flake8 + pylint)
2. ✅ Run unit tests with coverage
3. ✅ Build Docker image
```

### On Merge to `main`
```
1. ✅ All CI steps above
2. 📦 Push Docker image to GitLab Registry
3. 🚀 Deploy to production server (manual trigger)
```

---

## 📊 Monitoring Your Pipeline

### View Pipeline Status
- Go to **CI/CD → Pipelines** in GitLab
- Click on a pipeline to see job details

### View Test Results
- Click on `test` job
- Check coverage report in job artifacts

### View Docker Image
- Go to **Packages & Registries → Container Registry**
- Images are tagged with commit SHA and `latest`

---

## 🛠️ Manual Deployment (Alternative)

If you prefer manual deployment:

```bash
# On your server
cd /opt/patient-monitoring
chmod +x deploy.sh
sudo ./deploy.sh production
```

Or for staging:
```bash
sudo ./deploy.sh staging
```

---

## 🔐 Security Best Practices

### GitLab CI/CD Variables
- ✅ **Protect variables**: Only available on protected branches
- ✅ **Mask variables**: Hidden in job logs
- ✅ Never commit secrets to code

### Docker Image Security
- ✅ Images stored in private GitLab Registry
- ✅ Only authenticated users can pull
- ✅ Images tagged with commit SHA for traceability

### SSH Deployment
- ✅ Use SSH keys (not passwords)
- ✅ Restrict key to deployment user only
- ✅ Rotate keys periodically

---

## 🐛 Troubleshooting

### Pipeline Fails on Linting

```bash
# Fix linting issues locally
pip install flake8 pylint
flake8 Real-time\ data\ ingestion/ --count --select=E9,F63,F7,F82
pylint Real-time\ data\ ingestion/*.py
```

### Tests Fail

```bash
# Run tests locally
pip install -r requirements-dev.txt
pytest tests/ -v
```

### Docker Build Fails

```bash
# Build locally to debug
cd "Real-time data ingestion"
docker build -t test-app .
```

### Deployment Fails

Check job logs in GitLab, then:

```bash
# SSH into server manually
ssh user@your-server

# Check Docker status
docker compose ps
docker compose logs --tail=50 app

# Manual restart
cd /opt/patient-monitoring
docker compose up -d --build app
```

---

## 📈 Advanced Configuration

### Add Slack Notifications

Add to `.gitlab-ci.yml`:

```yaml
slack_notify:
  stage: .post
  image: curlimages/curl:latest
  script:
    - |
      curl -X POST -H 'Content-type: application/json' \
        --data '{"text":"Pipeline $CI_PIPELINE_STATUS: $CI_PROJECT_NAME"}' \
        $SLACK_WEBHOOK_URL
  rules:
    - if: '$CI_PIPELINE_SOURCE == "push"'
      when: always
```

### Add Email Notifications

GitLab sends email notifications automatically:
- **Settings → Notifications**

### Schedule Pipelines

Go to **CI/CD → Schedules** to create scheduled pipelines (e.g., nightly tests).

---

## 🎉 Success Checklist

- [ ] Code pushed to GitLab
- [ ] CI/CD variables configured
- [ ] SSH key added to server
- [ ] First pipeline runs successfully
- [ ] Docker image in registry
- [ ] Deployment successful
- [ ] Grafana accessible at `http://server-ip:3000`

---

## 📚 Additional Resources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitLab Container Registry](https://docs.gitlab.com/ee/user/packages/container_registry/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

**Need Help?** Check pipeline logs or run locally with `pytest` and `docker build`.
