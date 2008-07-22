from debshots.tests import *

class TestStartController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='start'))
        # Test response...
