import unittest
from sucuri import Files
from sucuri import rendering

template = rendering.template("test/testfile4.suc", {"book": "Hello! I'm here!"})

print(template)

