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
# Script to convert airfoil coordinate .dat files into SVG format, with minor
# additional attributes to make them easy to view in Inkscape.
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
import re
import argparse
import requests

UIUC_URL_FMT='http://m-selig.ae.illinois.edu/ads/coord/%s'

parser = argparse.ArgumentParser()
parser.add_argument("DAT", help="DAT file or DAT name (if using UIUC download)")
parser.add_argument("SCAD", nargs="?", help="OpenSCAD output file (defaults to <DAT>.scad)")
parser.add_argument("-u", "--url", help="Download the specified DAT name from the UIUC Airfoil Database", action="store_true")

args = parser.parse_args()

datfile=args.DAT
outfile=args.SCAD or "%s.scad" % (os.path.splitext(os.path.basename(datfile))[0])

# counter for the file header
count = 0

surfaces = []
current_surface = []

if args.url:
    if not datfile.endswith(".dat"):
        datfile = datfile + ".dat"

    url = UIUC_URL_FMT % (datfile)
    print "GET %s" % url
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
        lines = r.text.splitlines()
    else:
        raise "Error: %d response from %s" % (r.status_code, url)
else:
    with open(datfile) as f:
        lines = [l.strip() for l in f.readlines()]

# Strip off the 3-line header at the top of the file,
# then iterate through each line. If the line is blank
# start a new coordinate set (surface).
# For each line in the file, parse out a X, Y coordinate, amplified by the FACTOR
# and translated to the XLATE, YLATE offsets.
# Store each X,Y coordinate as a list of floats, in case we have to do further massaging.
for line in lines:
    if re.match('\s*[.0-9]+\s*[.0-9]+\s*', line) is None:
        continue
    elif len(line) < 3:
        surfaces.append(current_surface)
        current_surface = []
    else:
        xy = [float(str(s)) for s in re.split("\s*", line) if len(str(s)) > 0]
        # print xy
        if len(xy) > 1:
            current_surface.append(xy)

# Cleanup; add the last coordinate set we were working on to the list of coordinate sets.
surfaces.append(current_surface)

# Now, create an aggregated surface.
# Start with a copy of the first original surface, intact.
aggregated_surface = list(surfaces[0])

if len(surfaces) > 1:
    # Reverse the second set of coordinates and append them to the first.
    # This traces the second line (second surface) backward, starting from a 
    # point where the two surfaces connect on the trailing edge
    for coord in reversed(surfaces[1]):
        aggregated_surface.append(coord)

name = os.path.splitext(os.path.basename(datfile))[0]
with open(outfile, 'w') as f:
    f.write("// adapted from ")
    f.write(os.path.basename(datfile))
    f.write("\n\nmodule %s_airfoil(scale=1){\n    polygon(points=[" % name)
    first_coord = True
    for coord in aggregated_surface:
        if first_coord is True:
            first_coord = False
            f.write("\n        ")
        else:
            f.write(",\n        ")
        f.write("[scale * %s, scale * %s]" % (coord[0], coord[1]))
    
    f.write("\n    ]);\n}\n\n%s_airfoil(60);" % name)


