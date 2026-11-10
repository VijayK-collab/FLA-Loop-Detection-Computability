import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from loopcheck import *

def test_all():
    r = {name: check(p, regs, 5000, mod)[0] for name, p, regs, mod in DEMOS}
    v = list(r.values())
    assert v == [HALTS, LOOPS, UNKNOWN, LOOPS, HALTS], v

if __name__ == "__main__":
    test_all(); print("Task 4: all test cases passed")
