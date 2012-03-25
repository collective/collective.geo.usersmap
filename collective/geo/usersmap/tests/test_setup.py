# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.interface import directlyProvides
from zope.interface import Interface
from zope.component import queryMultiAdapter
from zope.component import getUtility

from Products.CMFPlone.utils import getToolByName
from plone.registry.interfaces import IRegistry

from layers import INTEGRATION_TESTING
from config import DEFAULT_MAP_TITLE
from config import DEFAULT_MAP_DESCRIPTION

from ..interfaces import IThemeSpecific
from ..interfaces import IUsersMapPreferences


class TestSetup(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        # marking the request
        directlyProvides(self.request, IThemeSpecific)

    def test_setup(self):
        pq = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(pq.isProductInstalled('collective.geo.bundle'))

    def test_maplayer(self):
        self.assertNotEquals(queryMultiAdapter(
                        (self.portal, self.request),
                                name='usersmap-layer'), None)

    def test_usersmap_view(self):
        self.assertNotEquals(queryMultiAdapter(
                        (self.portal, self.request),
                                name='usersmap_view'), None)

    def test_mapwidget_layers(self):
        user_map_view = queryMultiAdapter((self.portal, self.request),
                                                        name='usersmap_view')
        map_layers = queryMultiAdapter(
                (user_map_view, Interface, self.portal, Interface))
        self.assertTrue(u'usersmap' in [i.name for i in map_layers.layers()])

    def test_preferences(self):
        registry = getUtility(IRegistry)
        props = registry.forInterface(IUsersMapPreferences)

        self.assertEquals(props.title, DEFAULT_MAP_TITLE)
        self.assertEquals(props.description, DEFAULT_MAP_DESCRIPTION)
        self.assertEquals(props.user_properties, ['description', 'email'])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
