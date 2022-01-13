#!/usr/bin/python3
# ENTRYPOINT for Dockerfile

import io
import os
import shutil
import re
import unittest
from pathlib import Path
from util import clean_pyfile, send_feedback


SUBMISSION_DIR = Path(os.environ.get("SHARED_DIR", "/shared")) / "submission"
SUBMISSION_DEST_DIR = Path(os.environ.get("GRADER_DIR", "/grader")) / "submission"

SUBMISSION_DEST_DIR.mkdir(parents=True, exist_ok=True)


class CustomTestResult(unittest.TextTestResult):
    """Creates a cleaner output intended to be more suitable for grading feedback."""

    def addFailure(self, test, err):
        cls, e, tb = err
        if isinstance(e, AssertionError):
            e_str = ":".join(str(e).split(":")[1:]).strip()
            self.failures.append( (test, e_str) )
        else:
            super().addFailure(test, err)


def get_submission_files():
    """The primary rules for submission discovery are encoded here.

      - Submission files should be under $SHARED_DIR/submission. $SHARED_DIR defaults
        to `/shared` for Coursera platform support.
      - Files or paths with any component that starts with __ (double-underscore) are
        ignored.
      - File extensions must be one of supported: .csv, .json, .jsonl, .py, .txt
    """
    supported_suffixes = [".csv", ".json", ".jsonl", ".py", ".txt"]
    #loc = Path(os.environ.get("SHARED_DIR", "/shared")) / "submission"
    for path in SUBMISSION_DIR.glob("**/*"):
        if any([part.startswith("__") for part in path.parts]):
            continue
        if path.suffix in supported_suffixes: 
            yield(path)


def destination_for_submission(path):
    """Get the grading destination for a given submission file."""
    i = len(SUBMISSION_DIR.as_posix()) + 1
    dest = SUBMISSION_DEST_DIR / path.as_posix()[i:]
    return dest


def main(partId):
    #submission_location = os.environ.get("SUBMISSION_LOCATION", "/shared/submission/")
    #submission_file = None
    submissions = get_submission_files()
    for path in submissions:
        dest = destination_for_submission(path)
        if path.suffix == ".py":
            clean_pyfile(path, dest)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dest)
    try:
        submission_file = list(SUBMISSION_DEST_DIR.glob("*.py"))[0]
    except IndexError:
        msg = "Submission file not found"
        send_feedback(0.0, msg)
        return

    import tests # Deferred import to ensure submission prep is done first
    print("imported tests", tests)

    # Fail-fast tests are not scored
    if partId is None:
        print("No partId specified. Running all tests.")
        test_file_pattern = f"test*.py"
    else:
        print("Running tests for PartID:", partId)
        test_file_pattern = f"test_{partId}*.py"
    suite = unittest.defaultTestLoader.discover(Path(__file__).parent.resolve() / "tests", pattern=f"f{test_file_pattern}")
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, resultclass=CustomTestResult, failfast=True).run(suite)
    msg = stream.getvalue()
    stream.close()
    if result.errors or result.failures:
        # Send message and fail fast
        send_feedback(0.0, msg)
        print(msg)
        return

    # Standard tests
    suite = unittest.defaultTestLoader.discover(Path(__file__).parent.resolve() / "tests", pattern=test_file_pattern)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, resultclass=CustomTestResult, failfast=False).run(suite)
    errors = len(result.errors)
    failures = len(result.failures)
    total = result.testsRun
    print(f"{total} total tests run")
    correct = total - errors - failures
    if total > 0:
        score = correct / total
    else:
        score = 0.0  
    print(f'Score: {correct}/{total} = {score:.02}')
    print(f'Points: {score*25} / 25')
    msg = stream.getvalue()
    stream.close()
    if score < 1.0: 
        send_feedback(score, msg)
    else:
        send_feedback(score, "Your code passed all tests.")
    print(msg)


if __name__ == '__main__':
    part_id = os.environ.get("partId")
    try:
        main(part_id)
    except Exception as e:
        send_feedback(0.0, str(e))
        if os.environ.get("MODE", "").lower() == "debug":
            raise(e)
