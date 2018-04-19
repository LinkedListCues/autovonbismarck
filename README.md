# Documention for EECS 214 Auto Grader
#### Last Upated Spring 2018 by Ethan Robison

## Configuration
1. It's in Python3. If this bothers you because Python, then I justify my choice by saying accessibility. If this bothers you because "3," I say fuck right off Python 3 or b u s t.
2. You'll need a Canvas API key, and you'll need to put in in a file named "secret" in the same directory as `main.py`. I self-authenticated for this thing since I'm the only one who needs to run it. Presumably, you're doing the same.

## Overview of System

First, we configure the system to look at the right course and assignment.
Then we get a list of all of the students and make representations of each.
Then, we download each individual student's submission.
Then, we need to run our testing framework (MSTEST at the time of this writing; hopefully NUNIT in the future since it's cross-platform) on each submission solution.
We serialize out the results of the previous step.
Last, we need to take our test results (grades + comments) and upload them to Canvas. 
