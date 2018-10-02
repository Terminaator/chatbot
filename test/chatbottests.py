import unittest

class TestSimpleRequests(unittest.TestCase):

    def test_simpleQuestion(self):
        self.assertEqual('Tarkvaraprojekt on 6 eap.', 'Mitu eap on kursus tarkvaraprojekt?')


if __name__ == '__main__':
    unittest.main()