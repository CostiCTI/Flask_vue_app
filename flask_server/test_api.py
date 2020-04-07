import unittest
import sql_server

class Test(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_get_top(self):
        res = sql_server.get_top()
        l = res['result']
        isRevSorted = True
        for i in range(len(l) - 1):
            if l[i][1] < l[i+1][1]:
                isRevSorted = False
        self.assertTrue(isRevSorted)

    def test_calculate_level_1(self):
        level = sql_server.calculate_level(0)
        self.assertEqual(level, 0)
        level = sql_server.calculate_level(5)
        self.assertEqual(level, 1)
        level = sql_server.calculate_level(300)
        self.assertEqual(level, 5)
        level = sql_server.calculate_level(324)
        self.assertEqual(level, 5)
        level = sql_server.calculate_level(325)
        self.assertEqual(level, 6)
        level = sql_server.calculate_level(1000)
        self.assertEqual(level, 9)



if __name__ == '__main__':
    unittest.main()