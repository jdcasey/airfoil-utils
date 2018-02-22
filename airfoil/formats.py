
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

def _aggregate_surface(data):
    # Now, create an aggregated surface.
    # Start with a copy of the first original surface, intact.
    aggregated_surface = list(data['surfaces'][0])
    if len(data['surfaces']) > 1:
        # Reverse the second set of coordinates and append them to the first.
        # This traces the second line (second surface) backward, starting from a 
        # point where the two surfaces connect on the trailing edge
        for coord in reversed(data['surfaces'][1]):
            aggregated_surface.append(coord)

    # for coord in aggregated_surface:
    #     print "Aggregation includes point %s" % str(coord)

    return aggregated_surface


def write_scad(outfile, data, fname):
    with open(outfile, 'w') as f:
        f.write("// adapted from ")
        f.write(fname)
        f.write(" (%s)" % data['url'])
        f.write("\n\nmodule %s_airfoil(scale=100){\n    polygon(points=[" % fname)

        aggregated_surface = _aggregate_surface(data)

        first_coord = True
        for coord in aggregated_surface:
            if first_coord is True:
                first_coord = False
                f.write("\n        ")
            else:
                f.write(",\n        ")
            f.write("[scale * %s, scale * %s]" % (coord[0], coord[1]))
        
        f.write("\n    ]);\n}\n\n%s_airfoil();" % fname)


def write_svg(outfile, data, fname):
    aggregated_surface = _aggregate_surface(data)

    with open(outfile, 'w') as f:
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
     sodipodi:docname="%(fname)s.svg">
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
  <!-- Adapted from %(fname)s (%(url)s) -->
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
        d="m 0 0 L %(points)s z"
        id="path1"
        inkscape:connector-curvature="0"
        sodipodi:nodetypes="aaaaaaaaaaaaaaaaaaaaaaaaaaaassaaaaaa" />

</svg>
""" % ({'fname':fname,
        'url': data['url'], 
        'points': " L ".join([" ".join([str(val) for val in i]) for i in aggregated_surface])}))
