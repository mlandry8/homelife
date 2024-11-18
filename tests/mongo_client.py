import unittest

from unittest.mock import patch

class TestMongoClient(unittest.TestCase):
    @patch('')
    def test_get_client(self, mock_connect):
        pass
if __name__ == '__main__':
    unittest.main()