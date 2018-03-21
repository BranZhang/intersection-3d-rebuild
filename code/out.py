from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
from pyproj import Proj, transform

def output_data_to_file(road_data):
    stylename = 'blueLine'
    doc = KML.kml(
        KML.Document(
            KML.Name("yan an"),
            KML.Style(
                KML.LineStyle(
                    KML.color('FFF00014'),
                    KML.width('5.0')
                ),
                id=stylename
            )
        )
    )

    for road in road_data:
        pm = KML.Placemark(
            KML.name(road.road_id),
            KML.styleUrl('#{0}'.format(stylename)),
            KML.LineString(
                KML.extrude(0),
                GX.altitudeMode("absolute"),
                KML.coordinates(' '.join([turn_3857_project_to_4326(p) for p in road.points_with_z_value_list]))
            )
        )
        doc.Document.append(pm)

    f = open("model/test_yan_an4.kml", 'w')
    f.write(str(etree.tostring(doc)))
    f.close()

def turn_3857_project_to_4326(point):
    in_proj = Proj(init='epsg:3857')
    out_proj = Proj(init='epsg:4326')
    _x2, _y2 = transform(in_proj, out_proj, point.longitude, point.latitude)
    return '{0},{1},{2}'.format(_x2, _y2, point.altitude * 10)