from unittest import TestCase


class TestSimpleApp(TestCase):
    def test_print_message(self):
        self.assertEqual("Hello World", "Hello World")