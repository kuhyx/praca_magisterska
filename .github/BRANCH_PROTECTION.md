# Branch Protection Configuration

This document describes how to configure branch protection rules for the `main`/`master` branch to ensure all CI checks pass before merging pull requests.

## Required Status Checks

The repository has a CI workflow (`.github/workflows/main.yml`) that runs comprehensive tests across multiple configurations:
- **Compilers**: `lualatex`, `pdflatex`
- **Faculties**: `eiti`, `meil`
- **Languages**: `eng`, `pol`
- **Thesis Types**: `EngineerThesis`, `MasterThesis`

This creates 16 test matrix jobs (2×2×2×2) that must all pass before a pull request can be merged.

## Setting Up Branch Protection

### Via GitHub Web Interface

1. Navigate to your repository on GitHub
2. Click on **Settings** (requires admin permissions)
3. In the left sidebar, click **Branches**
4. Under "Branch protection rules", click **Add rule**
5. Configure the following settings:

   **Branch name pattern**: `main` (or `master` if that's your default branch)

   **Protect matching branches**:
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals (optional, recommended: 1)
   - ✅ **Require status checks to pass before merging**
     - ✅ Require branches to be up to date before merging
     - **Status checks that are required**:
       - Search for and select: `test (pdflatex, eiti, pol, MasterThesis)`
       - Search for and select: `test (pdflatex, eiti, pol, EngineerThesis)`
       - Search for and select: `test (lualatex, eiti, pol, MasterThesis)`
       - Search for and select: `test (lualatex, eiti, pol, EngineerThesis)`
       - Search for and select: `test (pdflatex, meil, pol, MasterThesis)`
       - Search for and select: `test (pdflatex, meil, pol, EngineerThesis)`
       - Search for and select: `test (lualatex, meil, pol, MasterThesis)`
       - Search for and select: `test (lualatex, meil, pol, EngineerThesis)`
       - Search for and select: `test (pdflatex, eiti, eng, MasterThesis)`
       - Search for and select: `test (pdflatex, eiti, eng, EngineerThesis)`
       - Search for and select: `test (lualatex, eiti, eng, MasterThesis)`
       - Search for and select: `test (lualatex, eiti, eng, EngineerThesis)`
       - Search for and select: `test (pdflatex, meil, eng, MasterThesis)`
       - Search for and select: `test (pdflatex, meil, eng, EngineerThesis)`
       - Search for and select: `test (lualatex, meil, eng, MasterThesis)`
       - Search for and select: `test (lualatex, meil, eng, EngineerThesis)`

   **Additional options** (recommended):
   - ✅ **Require conversation resolution before merging** (optional)
   - ✅ **Do not allow bypassing the above settings** (recommended)

6. Click **Create** or **Save changes**

### Via GitHub CLI (requires admin permissions)

```bash
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=test (pdflatex, eiti, pol, MasterThesis) \
  --field required_status_checks[contexts][]=test (pdflatex, eiti, pol, EngineerThesis) \
  --field required_status_checks[contexts][]=test (lualatex, eiti, pol, MasterThesis) \
  --field required_status_checks[contexts][]=test (lualatex, eiti, pol, EngineerThesis) \
  --field required_status_checks[contexts][]=test (pdflatex, meil, pol, MasterThesis) \
  --field required_status_checks[contexts][]=test (pdflatex, meil, pol, EngineerThesis) \
  --field required_status_checks[contexts][]=test (lualatex, meil, pol, MasterThesis) \
  --field required_status_checks[contexts][]=test (lualatex, meil, pol, EngineerThesis) \
  --field required_status_checks[contexts][]=test (pdflatex, eiti, eng, MasterThesis) \
  --field required_status_checks[contexts][]=test (pdflatex, eiti, eng, EngineerThesis) \
  --field required_status_checks[contexts][]=test (lualatex, eiti, eng, MasterThesis) \
  --field required_status_checks[contexts][]=test (lualatex, eiti, eng, EngineerThesis) \
  --field required_status_checks[contexts][]=test (pdflatex, meil, eng, MasterThesis) \
  --field required_status_checks[contexts][]=test (pdflatex, meil, eng, EngineerThesis) \
  --field required_status_checks[contexts][]=test (lualatex, meil, eng, MasterThesis) \
  --field required_status_checks[contexts][]=test (lualatex, meil, eng, EngineerThesis) \
  --field required_pull_request_reviews[required_approving_review_count]=1 \
  --field enforce_admins=true
```

## Verification

Once branch protection is enabled:
1. All pull requests to `main`/`master` will show the required status checks
2. The "Merge" button will be disabled until all 16 CI jobs pass
3. Pull requests must be up-to-date with the base branch before merging

## Testing Locally

Before pushing changes, you can test the LaTeX build locally:

```bash
cd latex
scons generate_tests
scons quick
```

This will verify that the basic build works before triggering the full CI matrix.

## Notes

- Branch protection rules can only be configured by repository administrators
- The status check names must match exactly as they appear in the GitHub Actions workflow
- Once configured, bypassing these rules requires admin override
- The CI workflow automatically runs on all push and pull request events
