# GitHub Actions CI/CD Configuration Guide

## Overview

This guide describes the GitHub Actions workflow configured to automatically run tests and perform security checks on every push to the repository.

---

## Workflow File

**Location:** `.github/workflows/test.yml`

The workflow is triggered automatically on:
- ✅ Push to `main` branch
- ✅ Push to `develop` branch
- ✅ Pull requests to `main` branch
- ✅ Pull requests to `develop` branch

---

## Workflow Jobs

### 1. Unit Tests Job
**Name:** `unit-tests`
**Runs on:** `ubuntu-latest`

**Responsibilities:**
- Sets up Python environment
- Installs dependencies
- Runs all unit tests with coverage analysis
- Generates coverage reports (XML, HTML, terminal)
- Uploads coverage to Codecov
- Archives test results and coverage reports

**Key Actions:**
```yaml
pytest tests/unit/ \
  -v \
  --tb=short \
  --cov=app \
  --cov-report=xml \
  --cov-report=html \
  --cov-report=term-missing \
  --junit-xml=test-results/unit-tests.xml
```

**Outputs:**
- `test-results/unit-tests.xml` - JUnit XML format for GitHub reporting
- `coverage.xml` - Coverage in Cobertura format for Codecov
- `htmlcov/` - HTML coverage report (archived)

**Status:** Must pass for integration tests to run

---

### 2. Integration Tests Job
**Name:** `integration-tests`
**Runs on:** `ubuntu-latest`
**Depends on:** `unit-tests` (must pass first)

**Responsibilities:**
- Sets up Python environment
- Installs dependencies
- Runs all integration tests
- Tests API endpoints
- Archives test results

**Key Actions:**
```yaml
pytest tests/integration/ \
  -v \
  --tb=short \
  --junit-xml=test-results/integration-tests.xml
```

**Outputs:**
- `test-results/integration-tests.xml` - JUnit XML results

**Status:** Must pass for security scanning

---

### 3. End-to-End Tests Job
**Name:** `e2e-tests`
**Runs on:** `ubuntu-latest`
**Depends on:** `unit-tests` (must pass first)

**Responsibilities:**
- Sets up Python environment
- Installs dependencies
- Installs Playwright browser
- Runs E2E tests with browser automation
- Archives test results

**Key Actions:**
```yaml
pytest tests/e2e/ \
  -v \
  --tb=short \
  --junit-xml=test-results/e2e-tests.xml \
  -m e2e
```

**Outputs:**
- `test-results/e2e-tests.xml` - JUnit XML results

**Note:** Runs in parallel with integration tests

---

### 4. Code Quality & Linting Job
**Name:** `code-quality`
**Runs on:** `ubuntu-latest`
**Runs in parallel with:** Other jobs

**Responsibilities:**
- Checks code formatting with Black
- Verifies import organization with isort
- Runs Pylint analysis
- Runs Flake8 style checks

**Tools Used:**
- **Black** - Code formatter
- **isort** - Import organizer
- **Pylint** - Code analyzer
- **Flake8** - Style checker

**Key Actions:**
```bash
# Check Black formatting
black --check app/ main.py tests/

# Check import sorting
isort --check-only app/ main.py tests/

# Run Pylint
pylint app/operations/__init__.py main.py

# Run Flake8
flake8 app/ main.py tests/ --max-line-length=100 --count
```

**Status:** Non-blocking (does not prevent deployment)

---

### 5. Test Results Summary Job
**Name:** `test-summary`
**Runs on:** `ubuntu-latest`
**Depends on:** All test jobs
**Runs:** Always (even if tests fail)

**Responsibilities:**
- Downloads all test artifacts
- Displays comprehensive test summary
- Verifies result files exist

**Output:**
```
📊 Test Execution Summary
================================
Unit Tests: Completed
Integration Tests: Completed
E2E Tests: Completed

✓ Unit test results available
✓ Integration test results available
✓ E2E test results available
```

---

### 6. Docker Build & Security Scan Job
**Name:** `security`
**Runs on:** `ubuntu-latest`
**Depends on:** `unit-tests`, `integration-tests`

**Responsibilities:**
- Builds Docker image
- Scans for vulnerabilities using Trivy
- Uploads results to GitHub Security tab

**Key Actions:**
```bash
# Build Docker image
docker build -t app:test .

# Scan with Trivy
trivy image-ref: 'app:test' --format sarif
```

**Vulnerability Scanner:** Trivy by Aqua Security
- Scans for known vulnerabilities in dependencies
- Generates SARIF format for GitHub integration
- Results appear in repository Security tab

---

### 7. Deployment Job (Production)
**Name:** `deploy`
**Runs on:** `ubuntu-latest`
**Depends on:** `unit-tests`, `integration-tests`, `security`
**Triggered only on:** Main branch push (not on pull requests)
**Environment:** Production

**Responsibilities:**
- Sets up Docker Buildx
- Authenticates with Docker Hub
- Builds and pushes Docker image
- Tags with both `latest` and commit SHA

**Key Actions:**
```yaml
docker build-push-action:
  push: true
  tags:
    - ${{ secrets.DOCKERHUB_USERNAME }}/is218-module8:latest
    - ${{ secrets.DOCKERHUB_USERNAME }}/is218-module8:${{ github.sha }}
  platforms: linux/amd64,linux/arm64
```

**Platforms:** Multi-platform build (AMD64 + ARM64)

---

## Workflow Execution Flow

```
┌─────────────────────────────────────────────────────────┐
│ Push to main/develop or Pull Request                    │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
    Unit Tests              Code Quality & Linting
        │                           │
        ├─ Pass?                    └─ No blocking
        │   │
        │   ├─ Yes ◄───────────────────┐
        │   │                          │
        │   └─► Integration Tests      │
        │        │                     │
        │        ├─ Pass?              │
        │        │   │                 │
        │        │   ├─ Yes ◄──────────┤
        │        │   │                 │
        │        └─► E2E Tests         │
        │             │                │
        │             ├─ Pass?         │
        │             │   │            │
        │             │   ├─ Yes ◄────┤
        │             │   │            │
        │             └─► Security     │
        │                  │           │
        │                  ├─ Pass?    │
        │                  │   │       │
        │                  │   ├─ Yes ◄┤
        │                  │   │       │
        │                  └─► Deploy (main only)
        │
        └─ No: Stop / Fail the check
```

---

## Artifacts & Reports

### Generated Artifacts

1. **Unit Test Results**
   - File: `unit-test-results/unit-tests.xml`
   - Format: JUnit XML
   - Retention: 30 days

2. **Integration Test Results**
   - File: `integration-test-results/integration-tests.xml`
   - Format: JUnit XML
   - Retention: 30 days

3. **E2E Test Results**
   - File: `e2e-test-results/e2e-tests.xml`
   - Format: JUnit XML
   - Retention: 30 days

4. **Coverage Report**
   - File: `coverage-report/` (HTML)
   - Format: HTML coverage visualization
   - Retention: 30 days

### Coverage Upload

Coverage reports are automatically uploaded to [Codecov](https://codecov.io):
- **Requires:** `CODECOV_TOKEN` repository secret (optional)
- **Location:** https://codecov.io/gh/tatejones2/is218-module8assignment
- **Reports:** Code coverage per commit

---

## Environment Variables

```yaml
PYTHON_VERSION: '3.10'
CACHE_VERSION: v1
```

These are defined at the workflow level for consistency across all jobs.

---

## Required Secrets

For deployment to work, add these secrets to your GitHub repository:

1. **DOCKERHUB_USERNAME**
   - Your Docker Hub username
   - Used for: Docker image push
   - How to set: Repository Settings → Secrets → New repository secret

2. **DOCKERHUB_TOKEN**
   - Docker Hub access token (with push permissions)
   - Used for: Docker authentication
   - How to set: Repository Settings → Secrets → New repository secret

**To create Docker Hub token:**
1. Go to Docker Hub account settings
2. Security → New Access Token
3. Name it (e.g., "GitHub Actions")
4. Copy the token
5. Add to GitHub as `DOCKERHUB_TOKEN`

---

## GitHub Environment Protection

The `deploy` job uses a GitHub environment called `production` for additional protection:

**Purpose:**
- Adds review requirement before deployment
- Only allows deployment from main branch
- Requires all tests to pass

**To configure:**
1. Repository Settings → Environments → Create/Edit "production"
2. Add protection rules:
   - Require reviewers (optional)
   - Only deployments from main allowed
   - Set deployment branches

---

## Workflow Trigger Events

The workflow runs on:

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
```

### When It Runs:

1. **On Push to Main**
   - All jobs run
   - If all pass, deployment is triggered

2. **On Push to Develop**
   - All jobs run except deployment
   - Useful for testing CI/CD pipeline

3. **On Pull Request**
   - All jobs run
   - No deployment
   - Results visible in PR checks

---

## Viewing Results

### In GitHub UI:

1. **Actions Tab**
   - Shows all workflow runs
   - Click run to see detailed logs
   - Each job's status visible

2. **Pull Request Checks**
   - Shows pass/fail status
   - Click "Details" to see logs
   - Required checks prevent merge

3. **Security Tab**
   - Shows Trivy scan results
   - Vulnerability summary
   - SARIF report details

4. **Commits**
   - Status badge on commits
   - Click badge for details

### Interpreting Status Badges:

- ✅ **Green checkmark** - All checks passed
- ❌ **Red X** - One or more checks failed
- ⏳ **Yellow dot** - Checks in progress
- ⊘ **Neutral dot** - Skipped (e.g., no secrets)

---

## Failure Handling

### Unit Test Failures
- ❌ Stops integration and E2E tests
- ❌ Blocks deployment
- **Action:** Fix failing tests locally, push fix

### Integration Test Failures
- ❌ Stops E2E tests
- ❌ Blocks deployment
- **Action:** Debug integration issues, push fix

### E2E Test Failures
- ❌ Does not block deployment (runs in parallel)
- ⚠️ Indicates UI issues
- **Action:** Review and fix E2E tests

### Code Quality Issues
- ⚠️ Does not block anything (non-blocking)
- **Info only** - Shows style inconsistencies
- **Action:** Optional cleanup, not required

### Security Scan Failures
- ❌ Blocks deployment
- **Action:** Update dependencies, resolve vulnerabilities

---

## Optimization Tips

### Improve Speed

1. **Parallel Execution**
   - Unit, integration, and E2E run in parallel
   - Code quality runs independently
   - Reduces total workflow time

2. **Caching**
   - Dependencies cached between runs
   - Python and pip cache enabled
   - Docker layer caching in build

3. **Early Exit**
   - Unit tests run first
   - Failing unit tests stop other jobs
   - Saves CI/CD minutes

### Reduce Failure Rate

1. **Run Tests Locally First**
   ```bash
   pytest tests/ -v
   ```

2. **Check Code Quality**
   ```bash
   black --check app/ main.py tests/
   isort --check-only app/ main.py tests/
   ```

3. **Build Docker Locally**
   ```bash
   docker build -t app:test .
   ```

---

## Debugging Workflow Issues

### View Detailed Logs

1. Go to Actions tab
2. Click the failed workflow run
3. Click the failed job
4. Expand step details
5. See full command output

### Common Issues

**Issue:** Tests pass locally but fail on GitHub
**Solution:** 
- Check Python version matches
- Verify all dependencies in requirements.txt
- Check for environment variable issues

**Issue:** Docker build fails on GitHub
**Solution:**
- Ensure Dockerfile has correct syntax
- Check all files referenced exist
- Verify base image is correct

**Issue:** Deployment fails despite passing tests
**Solution:**
- Check DOCKERHUB_USERNAME/TOKEN are set
- Verify Docker Hub credentials are correct
- Check token has push permissions

---

## Maintenance

### Regular Tasks

1. **Monitor Workflow Runs**
   - Check Actions tab weekly
   - Review any failures
   - Fix issues promptly

2. **Update Dependencies**
   - Review Python packages quarterly
   - Update requirements.txt
   - Run tests after updates

3. **Update GitHub Actions**
   - Regularly update action versions
   - Check for deprecation notices
   - Plan for major version changes

---

## Performance Statistics

Typical workflow execution times:

| Job | Time |
|-----|------|
| Unit Tests | ~2-3 minutes |
| Integration Tests | ~1-2 minutes |
| E2E Tests | ~3-5 minutes |
| Code Quality | ~1 minute |
| Security Scan | ~2 minutes |
| Deployment | ~5-10 minutes |
| **Total** | **~5-10 minutes** |

*Times vary based on dependency installation and caching effectiveness*

---

## Summary

The GitHub Actions workflow provides:

✅ **Automated Testing** - Every push is tested automatically
✅ **Multiple Test Types** - Unit, integration, E2E coverage
✅ **Code Quality Checks** - Linting and formatting validation
✅ **Security Scanning** - Vulnerability detection with Trivy
✅ **Coverage Reports** - Codecov integration for tracking
✅ **Automatic Deployment** - To production when tests pass
✅ **Multi-platform Support** - AMD64 and ARM64 Docker images
✅ **Clear Failure Handling** - Tests stop workflow on failure

This ensures code quality and reliability while automating the entire CI/CD process.
