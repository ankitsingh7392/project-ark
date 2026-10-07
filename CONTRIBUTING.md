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

---

## Commit messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): Short description

Optional longer body explaining the why, not the what.
```

**Types:** `feat` · `fix` · `chore` · `docs` · `refactor` · `perf` · `test` · `ci` · `revert`

**Scope** (optional): the project or area affected — `ats`, `lexiscan`, `ci`

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
```

---

## Pull requests

### Title

PR titles must follow the same `type(scope): Description` format. This is enforced automatically — the PR title check will block merge if the format is wrong.

### Before opening

Run the local CI from the repo root and fix anything it reports:

```bash
make ci        # lint + tests for every app + secret scan
```

`make help` lists the individual targets. GitHub Actions is kept as a backstop
but is not the primary gate; the Makefile runs the same checks.

### Description

Fill in the PR template. The checklist at the bottom is not optional — every box should be ticked before requesting review.

### Size

Keep PRs focused. A PR that touches five unrelated things is five PRs. Reviewers read diffs, not intentions.

### Do not merge your own PR

Open the PR, make sure CI is green, then merge. If you are the sole contributor, a one-person review pass — reading the diff as if you were a reviewer — is still worth doing before merging.

---

## What not to commit

The following are blocked by `.gitignore` and pre-commit hooks. Do not attempt to force-add them:

- Secrets, API keys, tokens, passwords — use environment variables, never source
- Training data, PDFs, CSVs, Excel files — keep data out of source control
- Binary model files (`.bin`, `.kv`, `.npy`)
- macOS metadata (`.DS_Store`)
- Virtual environments (`.venv/`)
- IDE config (`.idea/`, `.vscode/`)

---

## Adding a new app

Read [`CONSTITUTION.md`](CONSTITUTION.md) for the principles and
[`CHECKLIST.md`](CHECKLIST.md) for what must be true before the project is done.

1. Create the directory under `apps/` with its own `pyproject.toml`, `uv.lock` and `.python-version` pinned to `3.12`. Each app locks dependencies independently — see [ADR 001](docs/adr/001-standalone-uv-project-per-module.md). Shared code goes in `libs/` only once two apps need it — see [ADR 002](docs/adr/002-apps-and-libs-layout.md).
2. Copy [`docs/templates/CHECKLIST.md`](docs/templates/CHECKLIST.md) into the project, set the project type, and work through it in the order given in `CHECKLIST.md` §0.2.
3. Add a `Makefile` with the targets defined in [`docs/standards/toolchain.md`](docs/standards/toolchain.md).
4. Add the app to every applicable job in `.github/workflows/ci.yml`.
5. Update the root `README.md`: add a row to the app table and a summary section.

---

## Setting up locally

```bash
git clone https://github.com/ankitsingh7392/project-ark.git
cd project-ark

# Install pre-commit hooks (one-time)
make hooks
```

Pre-commit runs automatically on every `git commit`: secret scanning and ruff lint + format.
