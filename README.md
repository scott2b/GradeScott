# GradeScott

No true Scotsman would grade programming assignments by hand. That's why there's GradeScott.

### - or -

Grade Scott, Marty! It's not 1985. Why are you still grading programming assignments by hand?


## About

Designed primarily as a template repository for creating new graders for the
[Coursera Autograder](https://github.com/coursera/coursera_autograder). Python is
currently the only supported assignment language. Some minor specifics are here for
handling .py downloads from Notebook platforms, as Google Colab is the primary driving
use case for this project, but things should generally work with Python code written
any old regular way.


The initial thrust of this project was based on the Python section of the
[Coursera programming assignments demo](https://github.com/coursera/programming-assignments-demo),
but the resulting approach to grading is much different. Graders in GradeScott are
simply unit test files designed to work with [Python unittest](https://docs.python.org/3/library/unittest.html).


## Quickstart

 1. Copy [this repository](https://github.com/scott2b/GradeScott) via the "Use this template" button.

 2. Add unit tests to the `grader/tests` folder. Use the following conventions:
    - Modules should be named to match `test_[PART_ID]*.py`, or `ftest_[PART_ID]*.py`
      for fail-fast tests, where `[PART_ID]` is the Part ID provided by Courera. Or
      simply `test*.py` and `ftest*.py` to get started without a Part ID.
    - Tests should `import submission` and reference tested components via that
      namespace. Currently, only a single-file .py submission is supported. This will
      probably change at some point.
    - Test classes should subclass `unittest.TestCase` and have testing methods
      with names that start with `test`.
    - It is recommended that you clearly and specifically name test methods in a way
      that they will be useful in feedback to students. By default, stack traces are
      not provided in order to make the feedback more succinct, so cohesive testing
      and clear naming conventions are essential.

 3. Place a submission `.py` file into a location specified by `$SUBMISSION_LOCATION`
    (relative to the root of the repository).

 4. Add grader to your `PYTHONPATH`: `export PYTHONPATH=$PYTHONPATH:grader`. Making
    imports work similarly within Docker and without is a bit wonky, and this seems
    like the easiest fix. I'm open to better ideas.

 4. Test the assignment by running `python -m grader.grade`

## Build the grading container for local execution

```
docker build -t grader .
```

## Execution via built container

E.g.:

```
coursera_autograder grade local grader ./submission "{\"partId\": \"${partId}\"}" --dst-dir .
```
