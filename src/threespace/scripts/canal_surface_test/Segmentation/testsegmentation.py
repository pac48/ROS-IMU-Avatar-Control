#!/usr/bin/env python

import unittest

import numpy

import segment


class TestDataContainer(unittest.TestCase):
    def setUp(self):
        self.x = numpy.array([1, 2, 3])
        self.y = numpy.array([4, 5, 6])
        self.x2 = numpy.array([4, 5, 6])
        self.y2 = numpy.array([6, 5, 4])

    def testinit(self):
        """construction from x and y data"""
        a = segment.DataContainer(self.x, self.y)
        self.assertTrue(numpy.all(self.x == a.x))
        self.assertTrue(numpy.all(self.y == a.y))

    def testxrange(self):
        """ xrange property """
        a = segment.DataContainer(self.x, self.y)
        self.assertEqual(a.xrange, (1, 3))

    def testcontainsx(self):
        a = segment.DataContainer(self.x, self.y)
        self.assertTrue(a.contains(2))

    def testfromtable(self):
        """class method for construction from table"""
        a = segment.DataContainer.fromtable(numpy.vstack((self.x, self.y)).T)
        self.assertTrue(numpy.all(self.x == a.x))
        self.assertTrue(numpy.all(self.y == a.y))

    def testfromfile(self):
        """class method to read data from file"""
        a = segment.DataContainer.fromfile('testdata/almostlinear.dat')

    def testsplit(self):
        """data can be split at a position"""
        d = segment.DataContainer.fromfile('testdata/almostlinear.dat')
        a, b = d.split(2)

    def testadd(self):
        """the + operator works as expected"""
        a = segment.DataContainer(self.x, self.y)
        b = segment.DataContainer(self.x2, self.y2)
        c = a + b
        self.assertTrue(numpy.all(c.x == numpy.append(self.x, self.x2)))
        self.assertTrue(numpy.all(c.y == numpy.append(self.y, self.y2)))

    def testiadd(self):
        a = segment.DataContainer(self.x, self.y)
        b = segment.DataContainer(self.x2, self.y2)
        a += b
        self.assertTrue(numpy.all(a.x == numpy.append(self.x, self.x2)))
        self.assertTrue(numpy.all(a.y == numpy.append(self.y, self.y2)))


class TestLinearRegression(unittest.TestCase):
    def setUp(self):
        self.data = segment.DataContainer.fromfile('testdata/almostlinear.dat')

    def testInit(self):
        "Create fit object"
        self.fitter = segment.LinearRegression(self.data)

    def testFit(self):
        "Realistic linear fit"
        self.testInit()
        self.assertEqual(len(self.fitter.coeff), 2, "Linear fit has two coefficients")
        self.assertLess(self.fitter.error, 0.05, "Fit error is too large")


class TestTopDown(unittest.TestCase):
    def setUp(self):
        self.data = segment.DataContainer.fromfile('testdata/almostlinear.dat')

    def testTopDown(self):
        s = segment.TopDown(segment.LinearRegression, 2)
        s.segment(self.data)


class TestBottomUp(unittest.TestCase):
    def setUp(self):
        self.data = segment.DataContainer.fromfile('testdata/almostlinear.dat')

    def testBottomUp(self):
        s = segment.BottomUp(segment.LinearRegression, 2)
        s.segment(self.data)


class TestFitsSet(unittest.TestCase):
    def setUp(self):
        self.a = segment.LineThroughEndPoints(segment.DataContainer([1, 2], [1, 2]))
        self.b = segment.LineThroughEndPoints(segment.DataContainer([2, 3], [2, 1]))

    def testInit(self):
        s = segment.FitSet()

    def testAppend(self):
        s = segment.FitSet([self.a])
        self.assertTrue(len(s) == 1, "Construction failed to add one element")
        s.append(self.b)
        self.assertTrue(len(s) == 2, "Append failed to add one element")

    def testEvalSingle(self):
        s = segment.FitSet([self.a])
        self.assertAlmostEqual(s.eval(1.5), 1.5, 2, "Evaluation at single point failed")

    def testEvalMany(self):
        s = segment.FitSet([self.a, self.b])
        for x, expectedy in zip([1.5, 2.5], [1.5, 1.5]):
            self.assertAlmostEqual(s.eval(x), expectedy, 2, "Evaluation with multiple fits failed")

if __name__ == '__main__':
    unittest.main()
