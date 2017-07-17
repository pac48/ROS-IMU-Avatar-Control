#!/usr/bin/env python

from __future__ import print_function

import segment

# Create some data
data = segment.DataContainer([0, 1, 2, 3, 4], [0, 1, 2, 1, 0])

# Create a segmenter instance which fill fit 2 straight lines
segmenter = segment.TopDown(segment.LinearRegression, 2)

# do the fitting
fits = segmenter.segment(data)

# extract the two lines
line1, line2 = fits.fits

# Print a summary
print("I have fitted two lines to the data given in this table:")
for x, y in zip(data.x, data.y):
    print(x, y)

print("The overall error is", fits.error)
print("The fits are as follows:")
for i, fit in enumerate(fits.fits):
    print(i+1, "-", fit)

# plot a nice graph
fits.plot()
segment.plt.show()
