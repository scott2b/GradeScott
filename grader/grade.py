#!/usr/bin/python3
# ENTRYPOINT for Dockerfile

import io
import os
import shutil
import re
import unittest
from pathlib import Path
from util import clean_pyfile, send_feedback



class CustomTestResult(unittest.TextTestResult):
    """Creates a cleaner output intended to be more suitable for grading feedback."""

    def addFailure(self, test, err):
        cls, e, tb = err
        if isinstance(e, AssertionError):
            e_str = ":".join(str(e).split(":")[1:]).strip()
            self.failures.append( (test, e_str) )
        else:
            super().addFailure(test, err)


def main(partId):
    submission_location = os.environ.get("SUBMISSION_LOCATION", "/shared/submission/")
    submission_file = None
    for file_ in os.listdir(submission_location):
        if file_.endswith(".py"):
            submission_file = file_
        else:
            submission_file = None
    if submission_file is None:
        files = str(os.listdir(submission_location))
        _message = f"Files in submission location ({submission_location}): {files}"
        send_feedback(0.0, _message)
        return
    print(submission_file)
    sub_source = os.path.join(submission_location, submission_file)
    sub_destination = os.environ.get("SUBMISSION_DESTINATION", "/grader/submission.py")
    clean_pyfile(sub_source, sub_destination)
    try: # Test importing of submission
        import submission
    except ModuleNotFoundError as e:
        msg = "Attempted import of unsupported package. Error was: " + str(e)
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
