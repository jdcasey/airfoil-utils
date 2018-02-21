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

import click
import os
import airfoil.data as data
import airfoil.formats as formats

DEFAULT_SCALE=600
DEFAULT_X_TRANSLATE = 100
DEFAULT_Y_TRANSLATE = 200

@click.command()
@click.argument('DAT')
@click.option('--output', '-o', help='Output SVG path')
@click.option('--url', '-u', default=True, help='Download the specified DAT name from the UIUC Airfoil Database before attempting to read it', type=click.BOOL)
def foil2svg(dat, output, url=True):
    datfile=dat
    fname = (os.path.splitext(os.path.basename(datfile))[0])
    outfile=output or "%s.svg" % fname

    surfaces = data.load_surfaces(datfile, url)

    formats.write_svg(outfile, surfaces, fname)

@click.command()
@click.argument('DAT')
@click.option('--output', '-o', help='Output SCAD path')
@click.option('--url', '-u', default=True, help='Download the specified DAT name from the UIUC Airfoil Database before attempting to read it', type=click.BOOL)
def foil2scad(dat, output, url=True, x_translate=100, y_translate=200, scale=600):
    datfile=dat
    fname = (os.path.splitext(os.path.basename(datfile))[0])
    outfile=output or "%s.scad" % fname

    surfaces = data.load_surfaces(datfile, url)

    formats.write_scad(outfile, surfaces, fname)

@click.command()
@click.argument('DAT')
@click.option('--url', '-u', default=True, help='Download the specified DAT name from the UIUC Airfoil Database before attempting to read it', type=click.BOOL)
@click.option('--x-translate', '-x', default=DEFAULT_X_TRANSLATE, help='Translate to this X coordinate')
@click.option('--y-translate', '-y', default=DEFAULT_Y_TRANSLATE, help='Translate to this Y coordinate')
@click.option('--scale', '-s', default=DEFAULT_SCALE, help='Scale coordinates by this factor')
def foil2plot(dat, url=True, x_translate=100, y_translate=200, scale=600):
    datfile=dat
    fname = (os.path.splitext(os.path.basename(datfile))[0])

    surfaces = data.load_surfaces(datfile, url)

    import matplotlib.pyplot as plt

    xs = []
    ys = []
    for surface in surfaces:
        xs.append(x_translate + scale * surface[0])
        ys.append(y_translate - (scale * surface[1]))
    
    # plt.scatter(xs, ys)
    plt.axis('equal')
    plt.plot(xs, ys, linewidth=1)
    plt.show()
