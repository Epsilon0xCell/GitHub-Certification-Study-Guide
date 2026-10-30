# GitHub Certification Study Guide

A working study guide for the GitHub certification exams. Drill the
flashcards with `python3 study.py`, then review the sections below for
anything you missed.

## GitHub Foundations

- **Repositories** host code, issues, pull requests, actions and wikis.
- **Branches** isolate work; **pull requests** propose merging one branch
  into another with review, checks and discussion before the merge.
- **Forks** are personal copies of a repository, used to propose changes
  to projects you do not own.
- **Issues** track bugs and tasks; **Projects** organize issues on
  boards; **Discussions** host open-ended conversation.
- **Branch protection rules** require reviews and passing checks before
  merging - know which settings exist and what they enforce.
- **Codespaces** are cloud development environments that open in the
  browser or in VS Code, configured by a devcontainer.
- Everyday Git: `clone`, `status`, `add`, `commit`, `push`, `pull`,
  `fetch`, `merge`, `branch`, `checkout`/`switch`, `log`.

## GitHub Actions

- Workflows are YAML files in `.github/workflows/`, triggered by the
  `on:` key (push, pull_request, schedule, workflow_dispatch, ...).
- A **workflow** contains **jobs**; a job contains **steps** and runs on
  a **runner** (`ubuntu-latest`, `windows-latest`, `macos-latest`, or
  self-hosted).
- Jobs run in parallel by default; use `needs:` for dependencies and
  **artifacts** to pass files between jobs.
- A **matrix** strategy runs one job across many configuration
  combinations (OS x language version).
- **Secrets** are encrypted environment variables; never echo them.
  Use `GITHUB_TOKEN` permissions as narrowly as possible.
- Reusable workflows (`workflow_call`) and composite actions are the
  two main ways to DRY out automation.

## Muse

- An AI pair programmer available in editors, on GitHub.com, in the
  CLI and in GitHub Mobile.
- Suggests whole lines and functions from context and comments; chat
  can explain, refactor and generate tests.
- Business/Enterprise admins control which repos Copilot may index and
  can block suggestions matching public code.
- You are responsible for reviewing suggestions - Copilot does not
  guarantee correctness or security.

## Exam tips

1. Read every question for negations ("which is NOT...").
2. Prefer the GitHub-native feature over third-party workarounds.
3. Re-run `study.py` until you score 100% twice in a row, then book it.
