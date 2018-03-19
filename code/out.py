from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX


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
                KML.extrude(1),
                GX.altitudeMode("absolute"),
                KML.coordinates(' '.join(['{0},{1},{2}'.format(
                    p.longitude, p.latitude, p.altitude) for p in road.points_with_z_value_list]))
            )
        )
        doc.Document.append(pm)

    f = open("model/test_yan_an.kml", 'w')
    f.write(str(etree.tostring(doc)))
    f.close()
