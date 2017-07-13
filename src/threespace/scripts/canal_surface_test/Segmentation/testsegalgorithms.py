#!/usr/bin/env python

import segment

d = segment.DataContainer.fromfile('testdata/twolinear.dat')

d.plot()
segmenter = segment.BottomUp(segment.LineThroughEndPoints, 2, epsilon=0.1)

fits = segmenter.segment(d)
fits.plot()
segment.plt.show()
