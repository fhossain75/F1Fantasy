import unittest
import algos


class MyTestCase(unittest.TestCase):
    def test_knapsack_recursion(self):
        # Race 1 data
        Points = [17, -20, 32, 2, -18, -20, 1, -20, 4, 20, -17, 12, 59, 8, 10, 25, -19, 16, 0, 29]
        Cost = [12, 8.8, 18.4, 6.7, 6, 7.2, 11.8, 6.2, 24.2, 6.4, 18, 25.9, 29, 7.3, 23, 21, 13.1, 8.1, 9.6, 28.4]
        Budget = 100

        Acutal = algos.knapsack_recursion(Points, Cost, Budget, len(Points))
        Expected = 169

        self.assertEqual(Acutal, Expected)

    def test_knapsack_memoization(self):

        # Race 2 data
        Points = [11, -16, 29, 20, 7, 11, -8, 11, -1, 2, 22, -12, 41, 24, 45, 30, 8, 17, 6, 30]
        Cost = [12.6, 8.2, 19, 6.1, 5.4, 6.6, 11.2, 5.6, 23.9, 7, 17.4, 25.6, 29.3, 7.5, 22.7, 21.1, 12.5, 8.7, 9, 28.5]
        Budget = 100

        Acutal = algos.knapsack_memoization(Points, Cost, Budget, len(Points))
        Expected = 187

        self.assertEqual(Acutal, Expected)


if __name__ == '__main__':
    unittest.main()
