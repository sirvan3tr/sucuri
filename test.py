import unittest
import timeit
from sucuri import Files
from sucuri import rendering


name = 'test/includefile.suc'
text_example = """
html
    body
        h1 Title
        a(href='#') This is my link
"""

template = rendering.template("test/textfile.suc", {"text": "Hello! I'm here!", "x": "My x var"})

def tt():
    rendering.template("test/textfile.suc", {"text": "Hello! I'm here!"})

t = timeit.timeit('tt()', number=2000, globals=globals())
print(t)
print(template)


class TestFiles(unittest.TestCase):
    def test_add_files(self):
        files = Files()
        name = 'test/inc/link.suc'
        files.add(name)

        self.assertEqual(["a(href='#') {text}"], files.get( name) )

    def test_inject(self):
        files = Files()
        param = {"text": "Hello!", "list": [1, 2, 3, 4]}

        name = 'test/includefile.suc'
        files.add(name)

        rendered = files.template(name, param)
        self.assertIn('<html>', rendered )
        self.assertIn('</html>', rendered )
        self.assertIn('<ul>', rendered )
        self.assertIn('</ul>', rendered )
        self.assertIn('<style>', rendered )
        self.assertIn('</style>', rendered )

        self.assertNotIn( 'test/inc/list', rendered )
        self.assertNotIn( '+link', rendered )
    
    def test_template(self):
        files = Files()
        param = {"text": "Hello!", "list": [1, 2, 3, 4]}

        name = 'test/includefile.suc'
        files.add( name )

        rendered = files.template( name, param )

        self.assertEqual( rendered, rendering.template(name, param) )
    
    def test_attr(self):
        """
        Given an element that has an attribute with brackets inside it, e.g.
        a function with arguments.
        """ 
        equalValue = '<div v:onclick="function(\'hello\')">Click me</div>'
        self.assertEqualFunction('test/testfile2.suc', equalValue)

    def test_attr(self):
        """
        Testing script includes
        """
        equalValue = '<div class="ten">Hello World!</div><script>function example() {    console.log(\'test\');}</script>'
        self.assertEqualFunction('test/testfile3.suc', equalValue)

    def test_insert(self):
        template = rendering.template("test/testfile4.suc", {"book": "The Voice of Authority"})
        template = template.replace('\n','') # For the sake of testing only
        self.assertEqual(template, "<div>The Voice of Authority</div>")

    def assertEqualFunction(self, fileDir: str, equalValue: str):
        template = rendering.template(fileDir)
        template = template.replace('\n','') # For the sake of testing only
        should_be = equalValue 
        self.assertEqual(template, should_be)

if __name__ == '__main__':
    unittest.main()
