from debshots.tests import *

class TestUploadController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='upload'))
        # Test response...
