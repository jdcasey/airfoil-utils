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

def _parse_names(dat, output, output_format):
    dat = os.path.splitext(os.path.basename(dat))[0]
    output=output or output_format % dat
    fname = os.path.splitext(os.path.basename(output))[0]

    return (dat,output,fname)

@click.command()
@click.argument('DAT')
@click.option('--output', '-o', help='Output SVG path')
@click.option('--database', '-d', default='uiuc', type=click.Choice(['uiuc', 'airfoildb']), help='Specify the online database from which the DAT name will be downloaded')
def foil2svg(dat, output, database):
    dat,output,fname=_parse_names(dat, output, "%s.svg")
    surface_data = data.load_surfaces(dat, database)
    formats.write_svg(output, surface_data, fname)

@click.command()
@click.argument('DAT')
@click.option('--output', '-o', help='Output SCAD path')
@click.option('--database', '-d', default='uiuc', type=click.Choice(['uiuc', 'airfoildb']), help='Specify the online database from which the DAT name will be downloaded')
def foil2scad(dat, output, database, x_translate=100, y_translate=200, scale=600):
    dat,output,fname=_parse_names(dat, output, "%s.scad")
    surface_data = data.load_surfaces(dat, database)
    formats.write_scad(output, surface_data, fname)

@click.command()
@click.argument('DAT')
@click.option('--database', '-d', default='uiuc', type=click.Choice(['uiuc', 'airfoildb']), help='Specify the online database from which the DAT name will be downloaded')
@click.option('--x-translate', '-x', default=DEFAULT_X_TRANSLATE, help='Translate to this X coordinate')
@click.option('--y-translate', '-y', default=DEFAULT_Y_TRANSLATE, help='Translate to this Y coordinate')
@click.option('--scale', '-s', default=DEFAULT_SCALE, help='Scale coordinates by this factor')
def foil2plot(dat, database, x_translate=100, y_translate=200, scale=600):
    surface_data = data.load_surfaces(dat, database)

    import matplotlib.pyplot as plt

    xs = []
    ys = []
    for surface in surface_data['surfaces']:
        xs.append(x_translate + scale * surface[0])
        ys.append(y_translate - (scale * surface[1]))
    
    # plt.scatter(xs, ys)
    plt.axis('equal')
    plt.plot(xs, ys, linewidth=1)
    plt.show()
