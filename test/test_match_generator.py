import unittest

from app.utils.create_matches import CreateMatches


class TestMatchGenerator(unittest.TestCase):
    def test_3_with_1(self):
        l = [['a1'],
             ['b1'],
             ['c1']]
        m = CreateMatches.create(l)
        r = [['c1', 'b1', 'a1']]
        self.assertListEqual(r, m)

    def test_2_with_2(self):
        l = [['a1', 'a2'],
             ['b1', 'b2']]
        r = [['b1', 'a1'],
             ['b2', 'a1'],
             ['b1', 'a2'],
             ['b2', 'a2']]
        m = CreateMatches.create(l)
        print(m)
        self.assertListEqual(r, m)
