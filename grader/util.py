import json
import re
import os
from pathlib import Path


LINE_RX = re.compile(r'(\s*)(.*)')
SHARED_PATH = Path(os.environ.get("SHARED_DIR", "/shared"))


def send_feedback(score, msg):
    """Writes a feedback structure to shared for exposure in Coursera."""
    post = {
        "fractionalScore": score,
        "feedback": msg
    }
    print(json.dumps(post))
    feedback_path = SHARED_PATH / "feedback.json"
    with feedback_path.open("w") as outfile: 
        json.dump(post, outfile)


def comment_line(line):
    m = LINE_RX.match(line)
    return m.group(1) + 'pass # ' + m.group(2)
    

def clean_pyfile(source, dest):
    """Prepare a .py file for grading. Cleans up some potential Notebook artifacts
    as well as provides a truncation point designated as: #~~ /autograde
    """
    fp = Path(source)
    if fp.suffix == '.py':
        with fp.open(encoding="utf8") as f:
            clean_fp = Path(dest)
            with clean_fp.open('w', encoding="utf8") as cleanfile:
                for line in f:
                    if line.lstrip(" '\"").startswith('#~~ /autograde'):
                        break
                    if line.lstrip().startswith("!"):
                        line = comment_line(line)
                    if line.strip().startswith('get_ipython'):
                        line = comment_line(line)
                    cleanfile.write(line)
    else:
        # dest = clean_submissions / fp.name
        shutil.copyfile(source, dest)
