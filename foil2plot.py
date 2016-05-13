#!/usr/bin/env python

#################################################################################
# This file is part of airfoil-utils.
#
# airfoil-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# airfoil-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with airfoil-utils.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
#
# VERY simple script to plot airfoil coordinates from a coordinate .dat file
# using matplotlib.
#
# Currently, this script has only been tested on files from:
#
# http://m-selig.ae.illinois.edu/ads/coord_database.html
#
# Author: John Casey (jdcasey@commonjava.org)
#
#################################################################################

import os
import sys
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
	print "Usage: %s <airfoil-dat-file>" % sys.argv[0]
	exit(1)

DAT=sys.argv[1]
Y_FACTOR = 1
X_FACTOR = 1

count = 0
xs = []
ys = []
with open(DAT) as f:
	for line in f:
		if count > 3 and len(line) > 3:
			xy = [float(i) for i in line.lstrip().rstrip().split(' ')]
			print xy
			if len(xy) > 1:
				xs.append(X_FACTOR * float(xy[0]))
				ys.append(Y_FACTOR * float(xy[1]))
		count +=1

# plt.scatter(xs, ys)
plt.axis('equal')
plt.plot(xs, ys, linewidth=1)
plt.show()
