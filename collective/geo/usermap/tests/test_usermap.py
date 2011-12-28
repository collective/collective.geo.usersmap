# -*- coding: utf-8 -*-
import unittest2 as unittest
from lxml import objectify

from zope.interface import directlyProvides
from zope.component import queryMultiAdapter
from Products.CMFPlone.utils import getToolByName

from collective.geo.geographer.interfaces import IGeoCoder

from layers import INTEGRATION_TESTING
from ..interfaces import IThemeSpecific
from ..utils import coordinate_transform


_USERS = [('user_1', 'User 1', 'Torino'),
    ('user_2', 'User 2', 'Genova'),
    ('user_3', 'User 3', 'Torino'),
    ('user_4', 'User 4', 'Torino'),
    ('user_5', 'User 5', 'Civitanova Marche, Italia'),
    ('user_6', 'User 6 - àèìòù', 'Milan')
]

_DESCR = """Lorem ipsum dolor sit amet, consectetur adipiscing
elit. Cras eleifend elit quis tellus auctor ut
viverra erat faucibus."""


class TestKml(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.regtool = getToolByName(self.portal, 'portal_registration')

        # add some users
        self.users = [self._add_user(username, fullname, location) \
                        for username, fullname, location in _USERS]

        # mark request
        directlyProvides(self.request, IThemeSpecific)

    def _add_user(self, username, fullname, location):
        _username = username.lower()
        user = self.regtool.addMember(_username, _username)
        user.setMemberProperties({'fullname': fullname,
                            'location': location,
                            'description': _DESCR})
        return user

    def test_users_location(self):
        geo = IGeoCoder(self.portal)
        coords = [geo.retrieve(i.getProperty('location')) for i in self.users]
        unique_coordinate = []
        #TODO: test unique coordinates
        processed_coords = [coordinate_transform(i[0][1], unique_coordinate) \
                                                            for i in coords]

        # each user have its coordinates
        self.assertEquals(len(self.users), len(unique_coordinate))
        self.assertEquals(len(self.users), len(processed_coords))

    def test_usermap_users(self):
        kml_view = queryMultiAdapter((self.portal, self.request),
                                                name='usersmap.kml')
        data = [i for i in kml_view.get_users()]
        self.assertEquals(len(data), len(_USERS))

        for el in data:
            self.assertTrue(el['fullname'] in [i[1] for i in _USERS])
            self.assertEquals(el['description'], _DESCR)

    def test_usermap_view(self):
        kml_view = queryMultiAdapter((self.portal, self.request),
                                                name='usersmap.kml')

        root = objectify.fromstring(kml_view().encode('utf8'))
        document = root.Document
        self.assertEquals(document.name, 'Plone users')
        self.assertTrue(hasattr(document, 'Style'))

        kml_style = root.Document.Style
        self.assertEquals(kml_style.attrib.get('id'), 'manicon')
        self.assertTrue(hasattr(kml_style, 'IconStyle'))

        placemarks = [i for i in root.Document.Placemark]
        self.assertEquals(len(placemarks), len(_USERS))

        attrs = ['name', 'description', 'styleUrl', 'Point']
        for el in placemarks:
            for at in attrs:
                self.assertTrue(hasattr(el, at))

            kml_username = getattr(el, 'name')
            if kml_username:
                self.assertTrue(kml_username.text.encode('utf8') \
                                            in [i[1] for i in _USERS])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestKml))
    return suite
