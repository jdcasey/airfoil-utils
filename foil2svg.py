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

if len(sys.argv) != 3:
	print "Usage: %s <airfoil-dat-file> <svg-file>" % sys.argv[0]
	exit(1)

DAT=sys.argv[1]
SVG=sys.argv[2]

# Amplify coordinates by this amount to make them visible
FACTOR=600

# Translate all X and Y coordinates by this amount to drop the SVG in from the edge of the document
XLATE=100
YLATE=200

# counter for the file header
count = 0

surfaces = []
current_surface = []
with open(DAT) as f:
	# Strip off the 3-line header at the top of the file,
	# then iterate through each line. If the line is blank
	# start a new coordinate set (surface).
	# For each line in the file, parse out a X, Y coordinate, amplified by the FACTOR
	# and translated to the XLATE, YLATE offsets.
	# Store each X,Y coordinate as a list of floats, in case we have to do further massaging.
	for line in f:
		line = line.lstrip().rstrip()
		if count > 3:
			if len(line) < 3:
				surfaces.append(current_surface)
				current_surface = []
			else:
				xy = [float(i) for i in line.split(' ')]
				# print xy
				if len(xy) > 1:
					current_surface.append((XLATE + FACTOR * float(xy[0]), YLATE -(FACTOR * float(xy[1]))))
		count +=1

# Cleanup; add the last coordinate set we were working on to the list of coordinate sets.
surfaces.append(current_surface)

# Now, create an aggregated surface.
# Start with a copy of the first original surface, intact.
aggregated_surface = list(surfaces[0])

# Reverse the second set of coordinates and append them to the first.
# This traces the second line (second surface) backward, starting from a 
# point where the two surfaces connect on the trailing edge
for coord in reversed(surfaces[1]):
	aggregated_surface.append(coord)

with open(SVG, 'w') as f:
	f.write("""
<svg xmlns:dc="http://purl.org/dc/elements/1.1/" 
     xmlns:cc="http://creativecommons.org/ns#" 
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
     xmlns:svg="http://www.w3.org/2000/svg" 
     xmlns="http://www.w3.org/2000/svg" 
     xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" 
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" 
     id="svg3039" 
     version="1.1" 
     inkscape:version="0.48.4 r9939" 
     width="1200" 
     height="900" 
     sodipodi:docname="%s.svg">
  <metadata id="metadata3045">
    <rdf:RDF>
      <cc:Work rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <defs
     id="defs3043" />
  <sodipodi:namedview
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1"
     objecttolerance="10"
     gridtolerance="10"
     guidetolerance="10"
     inkscape:pageopacity="0"
     inkscape:pageshadow="2"
     inkscape:window-width="1590"
     inkscape:window-height="1014"
     id="namedview3041"
     showgrid="false"
     inkscape:zoom="1"
     inkscape:cx="216.28659"
     inkscape:cy="508.45613"
     inkscape:window-x="0"
     inkscape:window-y="27"
     inkscape:window-maximized="0"
     inkscape:current-layer="svg3039" />
  <path style="fill:#b3b4d2"
	    d="m %s %s L %s z"
	    id="path1"
	    inkscape:connector-curvature="0"
	    sodipodi:nodetypes="aaaaaaaaaaaaaaaaaaaaaaaaaaaassaaaaaa" />

</svg>
""" % (os.path.basename(DAT).split('.')[0], XLATE, YLATE, " L ".join([" ".join([str(val) for val in i]) for i in aggregated_surface])))


