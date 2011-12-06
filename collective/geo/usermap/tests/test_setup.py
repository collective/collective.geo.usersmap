# -*- coding: utf-8 -*-
import unittest2 as unittest

from Products.CMFPlone.utils import getToolByName

# from zope.component import getUtility
# from plone.registry.interfaces import IRegistry

from layers import INTEGRATION_TESTING


class TestSetup(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_setup(self):
        pq = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(pq.isProductInstalled('collective.geo.usermap'))
        self.assertTrue(pq.isProductInstalled('collective.geo.mapwidget'))

    def test_views(self):
        import ipdb; ipdb.set_trace( )
        kmlusers-layer


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
