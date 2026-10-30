#!/usr/bin/env python3
"""GitHub Cert Study Guide - interactive flashcard quiz.

Drills multiple-choice questions for the GitHub Foundations, GitHub
Actions and Muse certification exams. Questions are shuffled,
answers are graded instantly, and missed questions are recapped at the
end so you know exactly what to re-study in GUIDE.md.

Usage:
    python3 study.py                 # all topics, 10 questions
    python3 study.py --topic actions # one topic
    python3 study.py --count 20      # longer session
"""
import argparse
import random
import sys

# (topic, question, [options], correct_index, explanation)
QUESTIONS = [
    ("foundations", "What is a pull request?",
     ["A request to delete a branch", "A proposal to merge changes from one branch into another",
      "A backup of a repository", "A type of issue label"], 1,
     "Pull requests propose merging one branch into another and enable review before merging."),
    ("foundations", "Which command uploads local commits to a remote repository?",
     ["git fetch", "git pull", "git push", "git clone"], 2,
     "git push sends your local commits to the remote."),
    ("foundations", "What does a GitHub Codespace provide?",
     ["A static website host", "A cloud development environment in the browser",
      "A package registry", "A CI runner for hire"], 1,
     "Codespaces are full development environments hosted in the cloud."),
    ("foundations", "Which file, placed in a repository, is rendered on the repo home page?",
     ["INDEX.md", "README.md", "HOME.md", "ABOUT.md"], 1,
     "GitHub renders README.md on the repository landing page."),
    ("foundations", "What is the purpose of branch protection rules?",
     ["To hide a branch from collaborators", "To require reviews/checks before merging",
      "To encrypt branch contents", "To speed up cloning"], 1,
     "Protection rules enforce reviews, status checks and other merge requirements."),
    ("actions", "Where are GitHub Actions workflows defined?",
     [".github/workflows/*.yml", "actions/config.json", ".workflows/main.yml", "ci/pipeline.txt"], 0,
     "Workflows are YAML files in .github/workflows/."),
    ("actions", "Which key defines the events that trigger a workflow?",
     ["when", "on", "triggers", "events"], 1,
     "The 'on' key lists triggering events such as push and pull_request."),
    ("actions", "What is a 'job' in GitHub Actions?",
     ["A single shell command", "A set of steps that execute on the same runner",
      "A paid GitHub plan", "A reusable workflow only"], 1,
     "A job is a set of steps running on one runner; jobs run in parallel by default."),
    ("actions", "How do you share data between steps in the same job?",
     ["Secrets", "Environment files / outputs and the workspace filesystem",
      "You cannot share data", "Artifacts only"], 1,
     "Steps in a job share the workspace and can pass outputs; artifacts share between jobs."),
    ("actions", "Which runner label gives a Linux environment hosted by GitHub?",
     ["linux-latest", "ubuntu-latest", "github-linux", "runner-linux"], 1,
     "ubuntu-latest is the standard GitHub-hosted Linux runner label."),
    ("copilot", "What is Muse?",
     ["A code hosting platform", "An AI pair programmer that suggests code in your editor",
      "A CI service", "A project board"], 1,
     "Copilot is an AI assistant that suggests code and explanations inside supported editors."),
    ("copilot", "Can Muse be used from the command line?",
     ["No, editor only", "Yes, via the Copilot CLI / gh extension",
      "Only on GitHub.com", "Only in Codespaces"], 1,
     "Copilot is available in editors, on GitHub.com, and via the CLI."),
    ("foundations", "What does 'forking' a repository do?",
     ["Deletes the original", "Creates your own copy of the repository under your account",
      "Locks the repository", "Merges all branches"], 1,
     "A fork is a personal copy you can change freely and propose changes back from."),
    ("actions", "What is a matrix strategy used for?",
     ["Encrypting secrets", "Running a job across combinations of configurations",
      "Scheduling cron jobs", "Caching dependencies"], 1,
     "A matrix runs the same job across e.g. multiple OS and language versions."),
    ("foundations", "Which GitHub feature tracks bugs and feature requests?",
     ["Discussions", "Issues", "Projects", "Gists"], 1,
     "Issues track bugs, tasks and feature requests; Projects organize them on boards."),
]
TOPICS = sorted({q[0] for q in QUESTIONS})


def run(questions):
    correct, missed = 0, []
    attempted = 0
    for i, (topic, question, options, answer, why) in enumerate(questions, 1):
        order = list(range(len(options)))
        random.shuffle(order)
        shuffled = [options[j] for j in order]
        right = order.index(answer)
        print(f"\n[{topic}] Q{i}: {question}")
        for n, option in enumerate(shuffled, 1):
            print(f"  {n}. {option}")
        try:
            raw = input("Your answer (number): ").strip()
        except EOFError:
            print()
            break
        attempted += 1
        if raw.isdigit() and int(raw) - 1 == right:
            correct += 1
            print("Correct!")
        else:
            print(f"Not quite - the answer was {right + 1}. {options[answer]}")
            missed.append((question, why))
        print(f"Why: {why}")
    if attempted:
        print(f"\nScore: {correct}/{attempted} ({correct / attempted:.0%})")
        if attempted < len(questions):
            print(f"Session ended early: {len(questions) - attempted} question(s) not answered.")
    else:
        print("\nNo questions answered.")
    if missed:
        print("\nReview these in GUIDE.md:")
        for question, why in missed:
            print(f"  - {question}\n    {why}")
    return 0


def positive_int(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid int value: {value!r}")
    if number < 1:
        raise argparse.ArgumentTypeError("--count must be at least 1")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description="GitHub certification flashcard quiz.")
    parser.add_argument("--topic", choices=TOPICS, help="limit to one topic")
    parser.add_argument("--count", type=positive_int, default=10, help="number of questions")
    args = parser.parse_args(argv)
    pool = [q for q in QUESTIONS if not args.topic or q[0] == args.topic]
    random.shuffle(pool)
    selected = pool[:args.count]
    if len(selected) < args.count:
        print(f"Only {len(selected)} question(s) available for this selection; asking all of them.")
    return run(selected)


if __name__ == "__main__":
    raise SystemExit(main())
