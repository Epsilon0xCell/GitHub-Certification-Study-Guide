![Intro banner](intro-banner.png)

![Github Certification Study Guide banner](assets/banner.png)

![Animated scene](scene.svg)

# GitHub-Certification-Study-Guide

Study material for the GitHub certification exams: a written guide in
`GUIDE.md` plus an interactive flashcard quiz in `study.py`.

![Heading plate](plate.svg)

![Major separator](separator-major.svg)

## Requirements

- Python 3, standard library only.

![Heading plate](plate.svg)

![Major separator](separator-major.svg)

## Running the quiz

```bash
python3 study.py                  # 10 mixed questions
python3 study.py --topic actions  # drill one exam area
python3 study.py --count 20       # longer session
python3 study.py --help           # show all flags
```

Verified behavior:

- The question bank holds 15 questions: 7 `foundations`, 6 `actions`,
  and 2 `copilot`. Questions and answer options are shuffled each run.
- `--topic` accepts only `actions`, `copilot`, or `foundations`; any
  other value is rejected by argparse with exit status 2.
- `--count` must be a positive integer; `0`, negative, or non-numeric
  values are rejected with exit status 2. If `--count` is larger than
  the selected pool (for example `--topic copilot`, which has only 2
  questions), the program prints how many questions are available and
  asks all of them.
- Each answer is graded instantly, the correct answer and an explanation
  are shown, and missed questions are recapped at the end with a pointer
  to review them in `GUIDE.md`.
- Answers are entered as the option number. Any other input, including
  an out-of-range number or a blank line, counts as a wrong answer for
  that question. That includes digit characters that look numeric but
  do not convert to an integer, such as a superscript two: they count
  as wrong instead of crashing the session, which is what happened
  before.
- Closing input early ends the session: EOF (for example Ctrl-D) and
  Ctrl-C both work. The score is reported out of the questions
  actually answered, with a note saying how many were not answered;
  if none were answered it prints `No questions answered.`

![Heading plate](plate.svg)

![Major separator](separator-major.svg)

## Tests

```bash
python3 -m unittest
```

17 tests in `test_study.py`: the question bank itself (15 questions,
7 foundations, 6 actions, 2 copilot, four options each, every correct
index in range), `--count` parsing, grading (correct, wrong, blank,
decimal, out of range, and the superscript two regression), early
exits by EOF and Ctrl-C with the score counted over attempted
questions only, the small pool note for `--topic copilot`, and the
command line exit codes.

![Heading plate](plate.svg)

![Major separator](separator-major.svg)

## Files

- `study.py` - the interactive quiz.
- `test_study.py` - the test suite.
- `GUIDE.md` - the written study guide covering GitHub Foundations,
  GitHub Actions, and Muse, plus exam tips.
- `assets/banner.png`, `assets/logo.png` - project branding.
- `LICENSE` - GPL-3.0.

![Minor separator](separator-minor.svg)

> Museum label, pinned under this panel: a bad topic or a bad count exits with status 2.
> Museum label: copilot holds only 2 questions, so a longer request prints how many exist and asks all of them.
> Museum label: a superscript two counts as a wrong answer instead of crashing the sitting.
