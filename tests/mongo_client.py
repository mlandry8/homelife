import unittest

from unittest.mock import patch, Mock


class TestMongoClient(unittest.TestCase):
    @patch("")
    def test_get_client(self, mock_client: Mock) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
