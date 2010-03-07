from debshots.tests import *

class TestPackageController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='package'))
        # Test response...
