"""
Example assignment
"""

# Example notebook artifact that is cleaned before testing:
!pip install requests

def add(x, y):
    """Implement this function to return the sum of x and y."""
    pass


###
# SOLUTION: Not for publication to course materials:
def add_solution(x, y):
    return x + y
add = add_solution
#
###


#~~ /autograde

# Nothing below here should get run by the autograder

# Testing out my function

assert add(1,2) == 3
