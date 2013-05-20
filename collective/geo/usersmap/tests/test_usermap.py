# -*- coding: utf-8 -*-
import unittest2 as unittest
from lxml import objectify

from zope.interface import directlyProvides
from zope.interface import implements
from zope.component import queryMultiAdapter
from zope.component import getUtility

from zope.event import notify

from Products.CMFPlone.utils import getToolByName
from plone.app.users.browser.interfaces import IAccountPanelForm
from plone.app.controlpanel.events import ConfigurationChangedEvent

from collective.geo.mapwidget.interfaces import IGeoCoder


from layers import INTEGRATION_TESTING
from config import DEFAULT_MAP_TITLE
from config import DEFAULT_MAP_DESCRIPTION
from config import USERS
from config import USER_DESCRIPTION

from ..interfaces import IThemeSpecific
from ..utils import coordinate_transform


class DummyContext(object):
    """Dummy class to simulate
    Account panel form context
    """
    implements(IAccountPanelForm)
    userid = None


class TestKml(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.regtool = getToolByName(self.portal, 'portal_registration')

        # add some users
        self.users = [self._add_user(username, fullname, location) \
                        for username, fullname, location in USERS]

        # mark request
        directlyProvides(self.request, IThemeSpecific)

    def _add_user(self, username, fullname, location):
        _username = username.lower()
        user = self.regtool.addMember(_username, _username)
        data = {'fullname': fullname,
                'location': location,
                'email': 'test@email.it',
                'description': USER_DESCRIPTION}
        user.setMemberProperties(data)

        context = DummyContext()
        context.userid = username
        notify(ConfigurationChangedEvent(context, data))
        return user

    def test_users_location(self):
        geo = getUtility(IGeoCoder)
        coords = [geo.retrieve(i.getProperty('location')) for i in self.users]
        unique_coordinate = []
        #TODO: test unique coordinates
        processed_coords = [coordinate_transform(i[0][1], unique_coordinate) \
                                                            for i in coords]

        # each user have its coordinates
        self.assertEquals(len(self.users), len(unique_coordinate))
        self.assertEquals(len(self.users), len(processed_coords))

    def test_usersmap_users(self):
        kml_view = queryMultiAdapter((self.portal, self.request),
                                                name='usersmap.kml')
        data = [i for i in kml_view.get_users()]
        self.assertEquals(len(data), len(USERS))

        for el in data:
            self.assertTrue(el['fullname'] in [i[1] for i in USERS])
            self.assertTrue(USER_DESCRIPTION in el['description'])

    def test_usersmap_view(self):
        kml_view = queryMultiAdapter((self.portal, self.request),
                                                name='usersmap.kml')

        root = objectify.fromstring(kml_view().encode('utf8'))
        document = root.Document
        self.assertEquals(document.name, DEFAULT_MAP_TITLE)
        self.assertEquals(document.description,
                    "<![CDATA[%s]]>" % DEFAULT_MAP_DESCRIPTION)
        self.assertTrue(hasattr(document, 'Style'))

        kml_style = root.Document.Style
        self.assertEquals(kml_style.attrib.get('id'), 'manicon')
        self.assertTrue(hasattr(kml_style, 'IconStyle'))

        placemarks = [i for i in root.Document.Placemark]
        self.assertEquals(len(placemarks), len(USERS))

        attrs = ['name', 'description', 'styleUrl', 'Point']
        for el in placemarks:
            for at in attrs:
                self.assertTrue(hasattr(el, at))

            kml_username = getattr(el, 'name')
            if kml_username:
                self.assertTrue(kml_username.text.encode('utf8') \
                                            in [i[1] for i in USERS])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestKml))
    return suite
