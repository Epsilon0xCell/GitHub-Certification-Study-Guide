"""Tests for study.py. Run with: python3 -m unittest"""

import argparse
import builtins
import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import study
from study import QUESTIONS, TOPICS, positive_int, run

ROOT = Path(__file__).resolve().parent


def run_cli(*args, stdin_bytes=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "study.py"), *args],
        input=stdin_bytes, capture_output=True, cwd=ROOT, timeout=30)


def drive(questions, replies):
    """Run run() with scripted input and identity option shuffling.

    With the shuffle held still, the correct reply for a question is
    its bank correct_index + 1, which is what the replies list uses.
    A reply may be an exception instance to raise from input().
    """
    queue = list(replies)

    def fake_input(prompt=""):
        item = queue.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item

    out = io.StringIO()
    with mock.patch.object(study.random, "shuffle", lambda seq: None), \
            mock.patch.object(builtins, "input", fake_input):
        with redirect_stdout(out):
            code = run(questions)
    return code, out.getvalue()


class BankTests(unittest.TestCase):
    def test_bank_shape_and_counts(self):
        self.assertEqual(len(QUESTIONS), 15)
        counts = {}
        for topic, _q, options, answer, _why in QUESTIONS:
            counts[topic] = counts.get(topic, 0) + 1
            self.assertEqual(len(options), 4)
            self.assertGreaterEqual(answer, 0)
            self.assertLess(answer, len(options))
        self.assertEqual(counts, {"foundations": 7, "actions": 6, "copilot": 2})
        self.assertEqual(TOPICS, ["actions", "copilot", "foundations"])


class PositiveIntTests(unittest.TestCase):
    def test_valid_values(self):
        self.assertEqual(positive_int("1"), 1)
        self.assertEqual(positive_int("20"), 20)

    def test_invalid_values_raise_argument_type_error(self):
        for bad in ("0", "-3", "abc", "2.5", "²"):
            with self.assertRaises(argparse.ArgumentTypeError, msg=bad):
                positive_int(bad)


class RunGradingTests(unittest.TestCase):
    def test_correct_answer_scores_full_marks(self):
        q = QUESTIONS[0]
        code, out = drive([q], [str(q[3] + 1)])
        self.assertEqual(code, 0)
        self.assertIn("Correct!", out)
        self.assertIn("Score: 1/1 (100%)", out)

    def test_wrong_answer_is_recapped(self):
        q = QUESTIONS[0]
        wrong = str((q[3] + 1) % 4 + 1)
        _code, out = drive([q], [wrong])
        self.assertIn("Not quite", out)
        self.assertIn("Score: 0/1 (0%)", out)
        self.assertIn("Review these in GUIDE.md:", out)

    def test_blank_decimal_and_out_of_range_count_as_wrong(self):
        qs = QUESTIONS[:3]
        _code, out = drive(qs, ["", "1.5", "99"])
        self.assertIn("Score: 0/3 (0%)", out)

    def test_superscript_two_counts_as_wrong_without_crashing(self):
        # Regression: the superscript two character passes isdigit()
        # but int() rejects it. It used to raise ValueError out of
        # run() and kill the session with a traceback.
        _code, out = drive(QUESTIONS[:1], ["²"])
        self.assertIn("Not quite", out)
        self.assertIn("Score: 0/1 (0%)", out)

    def test_spaces_around_a_number_are_fine(self):
        q = QUESTIONS[0]
        _code, out = drive([q], [f"  {q[3] + 1}  "])
        self.assertIn("Correct!", out)


class RunEarlyExitTests(unittest.TestCase):
    def test_eof_after_one_answer_scores_attempted_only(self):
        q = QUESTIONS[0]
        _code, out = drive(QUESTIONS[:2], [str(q[3] + 1), EOFError()])
        self.assertIn("Score: 1/1 (100%)", out)
        self.assertIn("Session ended early: 1 question(s) not answered.", out)

    def test_eof_immediately_reports_no_questions_answered(self):
        _code, out = drive(QUESTIONS[:2], [EOFError()])
        self.assertIn("No questions answered.", out)

    def test_ctrl_c_after_one_answer_ends_like_eof(self):
        q = QUESTIONS[0]
        code, out = drive(QUESTIONS[:2], [str(q[3] + 1), KeyboardInterrupt()])
        self.assertEqual(code, 0)
        self.assertIn("Score: 1/1 (100%)", out)
        self.assertIn("Session ended early", out)

    def test_ctrl_c_immediately_reports_no_questions_answered(self):
        _code, out = drive(QUESTIONS[:2], [KeyboardInterrupt()])
        self.assertIn("No questions answered.", out)


class MainTests(unittest.TestCase):
    def test_topic_pool_smaller_than_count_asks_all_and_says_so(self):
        queue = iter(["1", "1"])
        out = io.StringIO()
        with mock.patch.object(study.random, "shuffle", lambda seq: None), \
                mock.patch.object(builtins, "input", lambda prompt="": next(queue)):
            with redirect_stdout(out):
                code = study.main(["--topic", "copilot", "--count", "10"])
        self.assertEqual(code, 0)
        self.assertIn("Only 2 question(s) available", out.getvalue())


class CliTests(unittest.TestCase):
    def test_help_exits_0(self):
        proc = run_cli("--help")
        self.assertEqual(proc.returncode, 0)

    def test_bad_count_and_bad_topic_exit_2(self):
        self.assertEqual(run_cli("--count", "0").returncode, 2)
        self.assertEqual(run_cli("--topic", "bogus").returncode, 2)

    def test_superscript_answer_over_stdin_exits_0(self):
        proc = run_cli("--count", "1", stdin_bytes="²\n".encode("utf-8"))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn(b"Traceback", proc.stderr)
        self.assertIn(b"Score: 0/1", proc.stdout)

    def test_eof_over_stdin_exits_0(self):
        proc = run_cli("--count", "2", stdin_bytes=b"")
        self.assertEqual(proc.returncode, 0)
        self.assertIn(b"No questions answered.", proc.stdout)


if __name__ == "__main__":
    unittest.main()
