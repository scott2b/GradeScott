"""
Experimental runner to see if we can run the grader programmatically. Would be used,
e.g., to run from a web framework environment for assignment submission.
"""
import json
import subprocess

GRADER_CONTAINER = "grader"
SHARED_FOLDER = "./shared"
SUBMISSION_FOLDER = f"{SHARED_FOLDER}/submission"


submission_dest = SUBMISSION_FOLDER # TODO: submitted assignment should be placed into
                                    # a unique submission subfolder which would be
                                    # passed to the call to coursera_autograder


proc = subprocess.run([
    "coursera_autograder",
    "grade",
    "local",
    GRADER_CONTAINER,
    submission_dest,
    "{\"partId\": \"\"}",
    "--dst-dir",
    SHARED_FOLDER,
], capture_output=True)

print(proc.stdout)
print("="*30)
print(proc.stderr)

with open("shared/feedback.json") as f:
    feedback = json.load(f)
print(feedback)
