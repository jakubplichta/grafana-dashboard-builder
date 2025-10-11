# grafana-dashboard-builder - Development Tasks

This document tracks all development tasks for modernizing and improving the grafana-dashboard-builder project.

## Task Status Legend
- ⬜ Not Started
- 🔄 In Progress
- ✅ Completed
- 🔴 Blocked
- ⏸️ On Hold

---

## Phase 1: Code Modernization (High Priority)

### Task 1.1: Remove Python 2 Legacy Code
**Status:** ⬜ Not Started  
**Priority:** High  
**Estimated Effort:** 2-4 hours

**Subtasks:**
- [ ] Remove all `from __future__ import unicode_literals` statements
- [ ] Remove all `from __future__ import` statements
- [ ] Update string handling to Python 3 native strings
- [ ] Remove Python 2 compatibility shims
- [ ] Update README to reflect Python 3-only support

**Files to modify:**
- `grafana_dashboards/common.py`
- `grafana_dashboards/config.py`
- `grafana_dashboards/context.py`
- `grafana_dashboards/errors.py`
- `grafana_dashboards/exporter.py`
- `grafana_dashboards/parser.py`
- All files in `grafana_dashboards/components/`
- All files in `grafana_dashboards/client/`

---

### Task 1.2: Modernize Import System in common.py
**Status:** ⬜ Not Started  
**Priority:** High  
**Estimated Effort:** 1 hour

**Subtasks:**
- [ ] Remove conditional import for `imp.load_source`
- [ ] Use only `importlib` machinery for all Python versions
- [ ] Add proper docstrings to `load_source` function
- [ ] Add type hints to functions
- [ ] Update tests if any exist for this module

**Files to modify:**
- `grafana_dashboards/common.py`

**Test coverage:**
- [ ] Add unit tests for `load_source` function
- [ ] Add unit tests for `get_component_type` function

---

### Task 1.3: Add Type Hints Throughout Codebase
**Status:** ⬜ Not Started  
**Priority:** High  
**Estimated Effort:** 8-12 hours

**Subtasks:**
- [ ] Add type hints to `common.py`
- [ ] Add type hints to `config.py`
- [ ] Add type hints to `context.py`
- [ ] Add type hints to `errors.py`
- [ ] Add type hints to `exporter.py`
- [ ] Add type hints to `parser.py`
- [ ] Add type hints to `cli.py`
- [ ] Add type hints to all component modules
- [ ] Add type hints to all client modules
- [ ] Create `py.typed` marker file

**Dependencies:**
- Task 1.1 (Remove Python 2 legacy code)

---

### Task 1.4: Migrate to pyproject.toml
**Status:** ⬜ Not Started  
**Priority:** High  
**Estimated Effort:** 3-4 hours

**Subtasks:**
- [ ] Create `pyproject.toml` with project metadata
- [ ] Move dependencies from `setup.py` to `pyproject.toml`
- [ ] Configure build system (setuptools, hatchling, or poetry)
- [ ] Move tool configurations (pytest, coverage, etc.) to `pyproject.toml`
- [ ] Test installation from new configuration
- [ ] Update CI/CD workflows
- [ ] Keep `setup.py` as a shim for backward compatibility (optional)
- [ ] Update documentation

**Files to create:**
- `pyproject.toml`

**Files to modify/deprecate:**
- `setup.py` (can be removed or kept as shim)
- `tox.ini` (can be partially migrated)
- `.github/workflows/build.yml`

---

## Phase 2: Code Quality & Tooling (High Priority)

### Task 2.1: Add MyPy Type Checking
**Status:** ⬜ Not Started  
**Priority:** High  
**Estimated Effort:** 2-3 hours

**Subtasks:**
- [ ] Add `mypy` to dev dependencies
- [ ] Create `mypy.ini` or add config to `pyproject.toml`
- [ ] Configure mypy for strict mode
- [ ] Fix any type errors discovered
- [ ] Add mypy to CI/CD pipeline
- [ ] Add pre-commit hook for mypy

**Dependencies:**
- Task 1.3 (Add type hints)
- Task 1.4 (Migrate to pyproject.toml)

---

### Task 2.2: Add Pre-commit Hooks
**Status:** ⬜ Not Started  
**Priority:** High  
**Estimated Effort:** 2-3 hours

**Subtasks:**
- [ ] Create `.pre-commit-config.yaml`
- [ ] Add black for code formatting
- [ ] Add isort for import sorting
- [ ] Add flake8 or ruff for linting
- [ ] Add mypy for type checking
- [ ] Add bandit for security scanning
- [ ] Add trailing whitespace removal
- [ ] Add YAML/JSON validators
- [ ] Update CONTRIBUTING.md with pre-commit instructions
- [ ] Run on all files and fix issues

**Files to create:**
- `.pre-commit-config.yaml`

---

### Task 2.3: Improve Test Coverage
**Status:** ⬜ Not Started  
**Priority:** High  
**Estimated Effort:** 12-16 hours

**Subtasks:**
- [ ] Audit current test coverage
- [ ] Set minimum coverage threshold (e.g., 80%)
- [ ] Add tests for `common.py`
- [ ] Add tests for `config.py`
- [ ] Add tests for `context.py`
- [ ] Add tests for `parser.py`
- [ ] Add tests for `exporter.py`
- [ ] Add tests for client modules
- [ ] Add tests for component modules
- [ ] Add integration tests
- [ ] Configure coverage reporting in CI
- [ ] Add coverage badge to README

**Files to modify:**
- `tests/` directory structure
- `.github/workflows/build.yml` or create `test.yml`

---

### Task 2.4: Improve Linting Configuration
**Status:** ⬜ Not Started  
**Priority:** Medium  
**Estimated Effort:** 2-3 hours

**Subtasks:**
- [ ] Review existing lint configuration
- [ ] Consider migrating to ruff (faster alternative)
- [ ] Configure comprehensive rule set
- [ ] Fix all linting errors
- [ ] Add linting badge to README
- [ ] Ensure lint checks run in CI

**Files to modify:**
- `.github/workflows/lint.yml`
- `pyproject.toml` or lint config files

---

## Phase 3: Documentation (Medium Priority)

### Task 3.1: Improve Docstrings
**Status:** ⬜ Not Started  
**Priority:** Medium  
**Estimated Effort:** 8-10 hours

**Subtasks:**
- [ ] Choose docstring format (Google, NumPy, or Sphinx)
- [ ] Add module-level docstrings to all modules
- [ ] Add/improve function docstrings with parameters and return types
- [ ] Add/improve class docstrings
- [ ] Document exceptions raised
- [ ] Add usage examples in docstrings
- [ ] Configure documentation generator (Sphinx or mkdocs)

**All modules need attention**

---

### Task 3.2: Update Copyright Headers
**Status:** ⬜ Not Started  
**Priority:** Low  
**Estimated Effort:** 1 hour

**Subtasks:**
- [ ] Decide on copyright policy (update range or remove)
- [ ] Update all copyright headers consistently
- [ ] Consider using SPDX license identifiers

**Files to modify:**
- All Python source files

---

### Task 3.3: Add CHANGELOG.md
**Status:** ⬜ Not Started  
**Priority:** Medium  
**Estimated Effort:** 2 hours

**Subtasks:**
- [ ] Create `CHANGELOG.md` using Keep a Changelog format
- [ ] Document historical changes (if possible)
- [ ] Add automation for changelog updates
- [ ] Link from README

**Files to create:**
- `CHANGELOG.md`

---

### Task 3.4: Add CONTRIBUTING.md
**Status:** ⬜ Not Started  
**Priority:** Medium  
**Estimated Effort:** 3-4 hours

**Subtasks:**
- [ ] Create `CONTRIBUTING.md`
- [ ] Document development environment setup
- [ ] Document code style guidelines
- [ ] Document testing requirements
- [ ] Document commit message conventions
- [ ] Document PR process
- [ ] Add issue/PR templates
- [ ] Link from README

**Files to create:**
- `CONTRIBUTING.md`
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/PULL_REQUEST_TEMPLATE.md`

---

### Task 3.5: Enhance README
**Status:** ⬜ Not Started  
**Priority:** Medium  
**Estimated Effort:** 2-3 hours

**Subtasks:**
- [ ] Add badges (build status, coverage, version, license)
- [ ] Improve installation instructions
- [ ] Add quick start guide
- [ ] Add more usage examples
- [ ] Document all CLI options
- [ ] Add troubleshooting section
- [ ] Add link to full documentation
- [ ] Add contributing section

**Files to modify:**
- `README.md`

---

## Phase 4: Project Structure (Medium Priority)

### Task 4.1: Add __all__ Exports
**Status:** ⬜ Not Started  
**Priority:** Medium  
**Estimated Effort:** 2-3 hours

**Subtasks:**
- [ ] Add `__all__` to `grafana_dashboards/__init__.py`
- [ ] Add `__all__` to all submodule `__init__.py` files
- [ ] Document public API
- [ ] Ensure exports are consistent with documentation

**Files to modify:**
- All `__init__.py` files

---

### Task 4.2: Organize Imports Consistently
**Status:** ⬜ Not Started  
**Priority:** Medium  
**Estimated Effort:** 1-2 hours

**Subtasks:**
- [ ] Configure isort in pyproject.toml
- [ ] Run isort on all Python files
- [ ] Add isort to pre-commit hooks
- [ ] Add isort to CI checks

**Dependencies:**
- Task 2.2 (Add pre-commit hooks)

---

## Phase 5: Error Handling & Logging (Medium Priority)

### Task 5.1: Implement Structured Logging
**Status:** ⬜ Not Started  
**Priority:** Medium  
**Estimated Effort:** 4-6 hours

**Subtasks:**
- [ ] Audit current logging usage
- [ ] Add logging configuration
- [ ] Implement structured logging (JSON format option)
- [ ] Add appropriate log levels throughout codebase
- [ ] Add context to error messages
- [ ] Document logging configuration options
- [ ] Add logging examples to documentation

**Files to modify:**
- Multiple files across the codebase
- `cli.py` for logging configuration

---

### Task 5.2: Review Exception Hierarchy
**Status:** ⬜ Not Started  
**Priority:** Medium  
**Estimated Effort:** 2-3 hours

**Subtasks:**
- [ ] Review `errors.py`
- [ ] Ensure proper exception hierarchy
- [ ] Add more specific exception types if needed
- [ ] Document all custom exceptions
- [ ] Add examples of exception handling

**Files to modify:**
- `grafana_dashboards/errors.py`

---

### Task 5.3: Add Input Validation
**Status:** ⬜ Not Started  
**Priority:** Medium  
**Estimated Effort:** 4-6 hours

**Subtasks:**
- [ ] Add CLI input validation
- [ ] Add configuration file validation
- [ ] Consider using Pydantic for schema validation
- [ ] Add validation for YAML configs
- [ ] Add helpful error messages for invalid inputs
- [ ] Add tests for validation

**Files to modify:**
- `grafana_dashboards/cli.py`
- `grafana_dashboards/config.py`

---

## Phase 6: Security & Best Practices (Medium Priority)

### Task 6.1: Security Audit
**Status:** ⬜ Not Started  
**Priority:** Medium  
**Estimated Effort:** 3-4 hours

**Subtasks:**
- [ ] Run bandit security scanner
- [ ] Fix any security issues found
- [ ] Add bandit to CI pipeline
- [ ] Review secrets management
- [ ] Ensure sensitive data isn't logged
- [ ] Add warnings for plain text secrets in configs
- [ ] Document secure configuration practices

---

### Task 6.2: Dependency Security
**Status:** ⬜ Not Started  
**Priority:** Medium  
**Estimated Effort:** 2-3 hours

**Subtasks:**
- [ ] Audit current dependencies
- [ ] Update to latest stable versions
- [ ] Ensure Dependabot is properly configured
- [ ] Add security advisory monitoring
- [ ] Pin dependency versions appropriately
- [ ] Document dependency update process

**Files to modify:**
- `pyproject.toml` or `setup.py`
- `.github/dependabot.yml`

---

## Phase 7: CI/CD & Automation (Low Priority)

### Task 7.1: Optimize GitHub Actions
**Status:** ⬜ Not Started  
**Priority:** Low  
**Estimated Effort:** 3-4 hours

**Subtasks:**
- [ ] Review existing workflows
- [ ] Add test coverage reporting
- [ ] Add automatic version bumping
- [ ] Add automatic release notes generation
- [ ] Optimize workflow performance (caching, etc.)
- [ ] Add workflow for documentation deployment
- [ ] Add workflow status badges to README

**Files to modify:**
- `.github/workflows/build.yml`
- `.github/workflows/lint.yml`
- `.github/workflows/codeql.yml`

---

### Task 7.2: Add Version Management
**Status:** ⬜ Not Started  
**Priority:** Low  
**Estimated Effort:** 2-3 hours

**Subtasks:**
- [ ] Choose version management tool (bump2version, commitizen)
- [ ] Configure semantic versioning
- [ ] Add version bumping workflow
- [ ] Update documentation
- [ ] Add git tags for releases

**Files to create:**
- `.bumpversion.cfg` or similar

---

## Phase 8: Performance (Low Priority)

### Task 8.1: Add Performance Benchmarks
**Status:** ⬜ Not Started  
**Priority:** Low  
**Estimated Effort:** 6-8 hours

**Subtasks:**
- [ ] Identify critical performance paths
- [ ] Create benchmark suite
- [ ] Add benchmark tests
- [ ] Document baseline performance
- [ ] Add performance regression tests to CI
- [ ] Document performance characteristics

---

### Task 8.2: Consider Async Support
**Status:** ⬜ Not Started  
**Priority:** Low  
**Estimated Effort:** 16-20 hours

**Subtasks:**
- [ ] Analyze where async would benefit performance
- [ ] Design async API (backward compatible)
- [ ] Implement async HTTP client
- [ ] Add async/await for API calls
- [ ] Add tests for async functionality
- [ ] Document async usage
- [ ] Consider supporting both sync and async APIs

**Note:** This is a major change and should be carefully planned

---

## Quick Wins (Can be done anytime)

### Quick Win 1: Fix Obvious Issues
- [ ] Fix any TODO or FIXME comments in code
- [ ] Fix obvious bugs found during review
- [ ] Fix typos in documentation
- [ ] Remove dead/commented code

### Quick Win 2: Code Formatting
- [ ] Run black on entire codebase
- [ ] Run isort on entire codebase
- [ ] Ensure consistent line endings

### Quick Win 3: CI Badge Updates
- [ ] Add missing badges to README
- [ ] Ensure all badge URLs are correct

---

## Task Dependencies Graph
Phase 1 (Code Modernization) ├── 1.1 Remove Python 2 Legacy → 1.3 Add Type Hints ├── 1.3 Add Type Hints → 2.1 Add MyPy └── 1.4 Migrate to pyproject.toml → 2.2 Pre-commit hooks
Phase 2 (Code Quality) ├── 2.2 Pre-commit hooks → 4.2 Organize imports └── 2.1 MyPy → Must complete 1.3 first
Phase 3 (Documentation) └── All tasks are independent
Phase 4-8 └── Can be done in parallel with Phase 3


---

## Notes

- Tasks are organized by phase and priority
- Estimated efforts are approximate
- Some tasks can be split across multiple developers
- Review and adjust priorities based on project needs
- Update this document as tasks are completed
