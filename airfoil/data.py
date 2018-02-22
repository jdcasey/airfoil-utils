
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import re
import os

DBs={'uiuc': 'http://m-selig.ae.illinois.edu/ads/coord/%s',
     'airfoildb': 'http://airfoildb.com/airfoils/%s'
     }

def load_surfaces(datfile, database):
    if os.path.exists(datfile):
        with open(datfile) as f:
            lines = [l.strip() for l in f.readlines()]
    else:
        if not datfile.endswith(".dat"):
            datfile = datfile + ".dat"

        url = DBs[database] % (datfile)
        print "GET %s" % url
        r = requests.get(url)

        if r.status_code == requests.codes.ok:
            lines = r.text.splitlines()
        else:
            raise "Error: %d response from %s" % (r.status_code, url)

    # counter for the file header
    count = 0

    surfaces = []
    current_surface = []

    # Strip off the 3-line header at the top of the file,
    # then iterate through each line. If the line is blank
    # start a new coordinate set (surface).
    # For each line in the file, parse out a X, Y coordinate, amplified by the scale
    # and translated to the x_translate, y_translate offsets.
    # Store each X,Y coordinate as a list of floats, in case we have to do further massaging.
    for line in lines[2:]:
        if len(line) < 3:
            if len(current_surface) > 0:
                surfaces.append(current_surface)
                current_surface = []
        else:
            try:
                xy = [float(str(i)) for i in re.split("\s*,?\s*", line) if len(str(i)) > 0]
            except Exception as e:
                print("Problem decoding line \"%s\"" % line)
                raise e
            # print xy
            if len(xy) > 1:
                current_surface.append((float(xy[0]), float(xy[1])))

    # Cleanup; add the last coordinate set we were working on to the list of coordinate sets.
    if len(current_surface) > 0:
        surfaces.append(current_surface)

    # print "Got %s surfaces" % len(surfaces)
    # print_count = 0
    # for surface in surfaces:
    #     print "Surface #%s contains %s points" % (print_count, len(surface))
    #     print_count = print_count+1

    return {'surfaces': surfaces, 'url': url}
