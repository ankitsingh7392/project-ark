# Contributing

## Branching

Always branch off `main`. Never push directly to `main` — branch protection will block it.

```bash
git checkout main && git pull
git checkout -b feat/your-feature-name
```

Use the branch prefix that matches your change type:

| Prefix | When to use |
|--------|-------------|
| `feat/` | New project or feature |
| `fix/` | Bug fix |
| `refactor/` | Restructuring without behaviour change |
| `chore/` | Tooling, dependencies, config |
| `docs/` | Documentation only |
| `ci/` | CI/CD pipeline |
| `infra/` | Docker, infrastructure |

---

## Commit messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): Short description

Optional longer body explaining the why, not the what.
```

**Types:** `feat` · `fix` · `chore` · `docs` · `refactor` · `perf` · `test` · `ci` · `infra` · `revert`

**Scope** (optional): the project or area affected — `ats`, `lexiscan`, `review-classifier`, `infra`, `ci`

**Rules:**
- Subject line: imperative mood, starts with uppercase, no period at the end
- Keep the subject under 72 characters
- Use the body to explain *why*, not *what* — the diff already shows what changed

**Examples:**

```
feat(ats): Add PDF resume parsing via PyMuPDF
fix(lexiscan): Handle empty input without crashing
chore: Bump ruff to 0.4.0
docs: Update root README with new project structure
ci: Pin actions to SHA for supply chain security
infra(postgres): Add connection pooling config
```

---

## Pull requests

### Title

PR titles must follow the same `type(scope): Description` format. This is enforced automatically — the PR title check will block merge if the format is wrong.

### Description

Fill in the PR template. The checklist at the bottom is not optional — every box should be ticked before requesting review.

### Size

Keep PRs focused. A PR that touches five unrelated things is five PRs. Reviewers read diffs, not intentions.

### Do not merge your own PR

Open the PR, make sure CI is green, then merge. If you are the sole contributor, a one-person review pass — reading the diff as if you were a reviewer — is still worth doing before merging.

---

## What not to commit

The following are blocked by `.gitignore` and pre-commit hooks. Do not attempt to force-add them:

- Secrets, API keys, tokens, passwords — use `.env` files (see `.env.example` in each service)
- Training data, PDFs, CSVs, Excel files — keep data out of source control
- Binary model files (`.bin`, `.kv`, `.npy`)
- macOS metadata (`.DS_Store`)
- Virtual environments (`.venv/`)
- IDE config (`.idea/`, `.vscode/`)

---

## Adding a new project

1. Create the directory under `projects/` (or `automation/` for workflow agents)
2. Add a `README.md` — follow the structure of existing project READMEs
3. Add a `.gitignore` appropriate for the project type
4. Update the root `README.md`: add a row to the module table and a summary section
5. If it is a Python project managed by uv, add it to the `[tool.uv.workspace]` members in the root `pyproject.toml`

---

## Setting up locally

```bash
git clone https://github.com/ankitsingh7392/project-ark.git
cd project-ark

# Install pre-commit hooks (one-time)
pip install pre-commit && pre-commit install
```

Pre-commit runs automatically on every `git commit`: secret scanning, ruff lint + format, and shellcheck.
