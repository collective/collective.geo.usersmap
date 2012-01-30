from geopy.geocoders.google import GQueryError
from collective.geo.geographer.geocoder import GeoCoderUtility


DUMMY_DATA = [{'address': "Torino",
                'output': [(u'Turin, Italy', (1.1, 2.1))]},
            {'address': "Genova",
                'output': [(u'Genova, Italy', (3.1, 4.1))]},
            {'address': "Civitanova Marche, Italia",
                'output': [(u'Civitanova Marche,, Italy', (5.1, 6.1))]},
            {'address': "Milan",
                'output': [(u'Milan, Italy', (7.1, 8.1))]},
             ]


class DummyGeoCoder(GeoCoderUtility):

    def retrieve(self, address=None):
        for item in DUMMY_DATA:
            if address == item['address']:
                return item['output']
        raise GQueryError
