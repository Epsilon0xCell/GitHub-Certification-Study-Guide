![Github Cert Study Guide banner](assets/banner.png)

# Github-Cert-Study-Guide

Study material for the GitHub certification exams: a written guide in
`GUIDE.md` plus an interactive flashcard quiz in `study.py`.

## Requirements

- Python 3, standard library only.

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
  that question.
- Closing input early (EOF, for example Ctrl-D) ends the session. The
  score is reported out of the questions actually answered, with a note
  saying how many were not answered; if none were answered it prints
  `No questions answered.`

## Files

- `study.py` - the interactive quiz.
- `GUIDE.md` - the written study guide covering GitHub Foundations,
  GitHub Actions, and Muse, plus exam tips.
- `assets/banner.png`, `assets/logo.png` - project branding.
- `LICENSE` - GPL-3.0.
