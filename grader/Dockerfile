FROM ubuntu:18.04

RUN \
  apt-get update && \
  apt-get install -y python3 && \
  apt-get install -y python3-pip

RUN mkdir /grader
RUN mkdir /grader/solutions

COPY grade.py /grader/grade.py
COPY util.py /grader/util.py
ADD tests /grader/tests

COPY requirements-grader.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements-grader.txt


# Important: Docker images are run without root access on Coursera. Its important to setup permissions accordingly.
# Executable permissions: Required to execute grader.py
# Read/write permissions: Required to copy over the submission from shared/submission
RUN chmod a+rwx -R /grader/

# Setup the command that will be invoked when your docker image is run.
ENTRYPOINT ["grader/grade.py"]
