# GitHub Actions Troubleshooting & Quick Start Guide

## Quick Start

### First Time Setup

1. **Ensure tests pass locally:**
   ```bash
   pytest tests/ -v
   ```

2. **Push to GitHub:**
   ```bash
   git add -A
   git commit -m "Your message"
   git push origin main
   ```

3. **Monitor workflow:**
   - Go to repository → Actions tab
   - Click on the latest workflow run
   - Watch tests execute in real-time

### Viewing Results

**Actions Tab:**
- Shows all workflow runs
- Click run name to see details
- Each job shows pass/fail status

**Pull Request Checks:**
- Shows inline in PR
- Click "Details" to see full logs
- Required checks prevent merge

---

## Common Issues & Solutions

### Issue 1: Tests Pass Locally but Fail on GitHub

**Symptoms:**
```
FAILED tests/unit/test_calculator.py::test_add - AssertionError
```

**Common Causes:**
- Python version mismatch
- Missing dependencies
- Environment variable issues

**Solutions:**
```bash
# Check Python version
python --version  # Should be 3.10+

# Check requirements are installed
pip list | grep pytest

# Run tests in verbose mode
pytest tests/ -vv

# Try with same Python version as GitHub (3.10)
python3.10 -m pytest tests/
```

---

### Issue 2: Playwright Tests Timeout

**Symptoms:**
```
TimeoutError: page.goto: Target page, context or browser has been closed
```

**Common Causes:**
- Playwright browser not installed
- Server not started for E2E tests
- Test timeout too short

**Solutions:**
```bash
# Install Playwright browsers
playwright install chromium

# Run E2E tests with extended timeout
pytest tests/e2e/ -v --timeout=30

# Check if FastAPI server is running
ps aux | grep uvicorn
```

---

### Issue 3: Coverage Report Not Generated

**Symptoms:**
```
ERROR: no tests ran as collection failed
```

**Common Causes:**
- Test files not found
- Import errors in test files
- Missing `__init__.py` files

**Solutions:**
```bash
# Check test discovery
pytest --collect-only

# Verify __init__.py exists in test dirs
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
touch tests/e2e/__init__.py

# Run with verbose collection
pytest tests/ -vv
```

---

### Issue 4: Docker Build Fails

**Symptoms:**
```
ERROR: failed to solve with frontend dockerfile.v0: failed to build LLB
```

**Common Causes:**
- Dockerfile syntax error
- File not found (COPY/ADD commands)
- Base image issues

**Solutions:**
```bash
# Build locally to test
docker build -t app:test .

# Check Dockerfile syntax
docker run --rm -i hadolint/hadolint < Dockerfile

# Verify files referenced exist
ls -la requirements.txt
ls -la app/
```

---

### Issue 5: Deployment Token Issues

**Symptoms:**
```
ERROR: Cannot perform an interactive login. Use --username and --password to provide credentials.
```

**Common Causes:**
- DOCKERHUB_USERNAME or DOCKERHUB_TOKEN not set
- Token permissions insufficient
- Token expired

**Solutions:**

1. **Set secrets:**
   - Go to Repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`

2. **Verify token permissions:**
   - Go to Docker Hub → Account Settings → Security
   - Check token has "Read & Write" permissions
   - Regenerate if needed

3. **Test credentials locally:**
   ```bash
   docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_TOKEN
   docker push username/repo:test
   ```

---

## Debugging Workflow Runs

### View Full Logs

1. Go to **Actions** tab
2. Click the **failed workflow run**
3. Click the **failed job**
4. **Expand** the failed step
5. See full command output and errors

### Run Single Job

To test a single job without running the full workflow:

```bash
# Simulate unit test environment locally
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/unit/ -v --cov=app
```

### Debug Mode

Add debug output to workflow:

```yaml
- name: Debug Info
  run: |
    echo "Python version:"
    python --version
    echo "Installed packages:"
    pip list
    echo "Test discovery:"
    pytest --collect-only
```

---

## Performance Optimization

### Speed Up Tests

1. **Run tests in parallel:**
   ```bash
   pip install pytest-xdist
   pytest tests/ -n auto
   ```

2. **Skip slow tests in CI:**
   ```bash
   pytest tests/ -m "not slow"
   ```

3. **Cache dependencies:**
   ```yaml
   - uses: actions/cache@v3
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
   ```

### Reduce Workflow Time

- Unit tests run first (fail fast)
- Integration and E2E run in parallel
- Code quality runs independently
- Total time: ~5-10 minutes typical

---

## Log Analysis

### Find Errors in Logs

```bash
# Search for ERROR messages
grep "ERROR" logs/app.log

# Find timeout errors
grep "timeout" logs/app.log

# Count test results
grep "PASSED\|FAILED" test-results/unit-tests.xml
```

### Parse JUnit XML Results

```bash
# View XML results
cat test-results/unit-tests.xml

# Extract passed/failed counts
grep -o '<testcase' test-results/unit-tests.xml | wc -l
```

---

## Environment Variables

### Available in Workflow

```yaml
# GitHub provided
github.ref              # refs/heads/main
github.sha              # Commit SHA
github.event_name       # 'push' or 'pull_request'
github.actor            # Username of pusher
runner.os               # 'Linux'

# Workflow defined
PYTHON_VERSION: '3.10'
CACHE_VERSION: v1
```

### Use in Workflow

```yaml
- name: Show context
  run: |
    echo "Branch: ${{ github.ref }}"
    echo "Commit: ${{ github.sha }}"
    echo "Actor: ${{ github.actor }}"
```

---

## Test-Specific Issues

### Pytest Cannot Find Tests

**Solution:**
```bash
# Ensure test files exist
ls tests/unit/test_*.py

# Check __init__.py files
ls tests/__init__.py
ls tests/unit/__init__.py

# Run collection test
pytest --collect-only
```

### Import Errors in Tests

**Solution:**
```bash
# Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"

# Verify imports work
python -c "from app.operations import add"

# Check package structure
ls app/__init__.py  # Should exist
```

### Test Dependencies Missing

**Solution:**
```bash
# Verify requirements.txt
pip install -r requirements.txt

# Check specific package
pip show pytest

# Install test dependencies
pip install pytest pytest-cov pytest-xdist
```

---

## GitHub-Specific Features

### Branch Protection Rules

To enforce all checks pass before merge:

1. Go to **Settings** → **Branches**
2. Click **Add rule**
3. Select **Require status checks to pass**
4. Select:
   - `unit-tests`
   - `integration-tests`
   - `code-quality`
5. Save

### Workflow Status Badge

Add to README.md:

```markdown
[![CI/CD](https://github.com/tatejones2/is218-module8assignment/workflows/CI%2FCD%20-%20Automated%20Testing/badge.svg)](https://github.com/tatejones2/is218-module8assignment/actions)
```

### Codecov Coverage Badge

Add to README.md:

```markdown
[![codecov](https://codecov.io/gh/tatejones2/is218-module8assignment/branch/main/graph/badge.svg)](https://codecov.io/gh/tatejones2/is218-module8assignment)
```

---

## Best Practices

### Before Committing

```bash
# Run all tests locally
pytest tests/ -v

# Check code quality
black --check app/ main.py tests/
isort --check-only app/ main.py tests/
pylint app/operations/__init__.py main.py

# Build Docker image
docker build -t app:test .
```

### After Pushing

```bash
# Monitor workflow
watch -n 2 'curl -s https://api.github.com/repos/tatejones2/is218-module8assignment/actions/runs | jq ".workflow_runs[0] | .status"'

# Or manually check
# Go to https://github.com/tatejones2/is218-module8assignment/actions
```

### Commit Message Conventions

```bash
# Include test info in message
git commit -m "Add feature X

- Passes all unit tests
- Integration tests updated
- E2E tests added"
```

---

## Useful Commands

### Trigger Workflow Manually

```bash
# Push to trigger workflow
git push origin main

# Or make empty commit to trigger
git commit --allow-empty -m "Trigger workflow"
git push origin main
```

### Check Workflow Status

```bash
# Via GitHub CLI (if installed)
gh run list

gh run view <run-id> --log

# View specific job logs
gh run view <run-id> --job <job-id>
```

### Download Artifacts

```bash
# Via GitHub CLI
gh run download <run-id>

# Check available artifacts
gh run view <run-id> --json artifacts
```

---

## Production Deployment Checklist

Before merging to main (deployment branch):

- [ ] All unit tests pass locally
- [ ] All integration tests pass locally
- [ ] All E2E tests pass locally
- [ ] Code quality checks pass
- [ ] Coverage report reviewed
- [ ] Docker builds successfully locally
- [ ] No new warnings or errors
- [ ] README updated if needed
- [ ] CHANGELOG updated
- [ ] All commits have meaningful messages

---

## Support & Resources

### GitHub Actions Documentation
- https://docs.github.com/en/actions

### Pytest Documentation
- https://docs.pytest.org/

### Docker Documentation
- https://docs.docker.com/

### Trivy Scanner
- https://github.com/aquasecurity/trivy

### Repository Actions
- https://github.com/tatejones2/is218-module8assignment/actions

---

## Summary

GitHub Actions provides:
- ✅ Automatic test execution on push
- ✅ Immediate feedback on code quality
- ✅ Security scanning integration
- ✅ Coverage tracking
- ✅ Automated deployment
- ✅ Audit trail of all changes

Use the troubleshooting guide to resolve issues quickly and keep the pipeline running smoothly!
