# -*- coding: utf-8 -*-
import unittest2 as unittest
from layers import INTEGRATION_TESTING

from zope.interface import directlyProvides
from zope.component import queryUtility
from Products.CMFPlone.utils import getToolByName

from ..interfaces import IThemeSpecific
from ..interfaces import IUsersCoordinates
from ..registry import UsersCoordinates


class TestUtility(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, IThemeSpecific)

    def test_utility(self):
        self.assertIsNotNone(queryUtility(IUsersCoordinates))

    def test_tool(self):
        self.assertIsNotNone(
                getToolByName(self.portal, 'portal_userscoordinates', None))

    def test_add_user(self):
        tool = UsersCoordinates(id='portal_userscoordinates')
        data = {'userid': 'giorgio',
                'fullname': "Giorgio Borelli",
                'description': 'test description',
                'location': 'Torino'}
        tool.add(**data)
        ud = tool.get(data['userid'])
        self.assertIsNotNone(ud)
        for k, v in data.items():
            self.assertEquals(v, ud.get(k))
        # see: c.geo.usersmap.tests.adapters DUMMY_DATA
        self.assertEquals(ud.get('coordinates'), (1.1, 2.1))

    def test_update_user(self):
        tool = UsersCoordinates(id='portal_userscoordinates')
        data = {'userid': 'giorgio',
                'fullname': "Giorgio Borelli",
                'description': 'test description',
                'location': 'Torino'}

        tool.add(**data)
        new_data = {'location': 'Milan',
                    'fullname': 'Mario Rossi',
                    }
        data.update(new_data)
        tool.update(**data)
        ud = tool.get(data['userid'])

        self.assertIsNotNone(ud)
        for k, v in new_data.items():
            self.assertEquals(v, ud.get(k))
        # see: c.geo.usersmap.tests.adapters DUMMY_DATA
        self.assertEquals(ud.get('coordinates'), (7.1, 8.1))

    def test_update_user_without_location(self):
        tool = UsersCoordinates(id='portal_userscoordinates')
        data = {'userid': 'giorgio',
                'fullname': "Giorgio Borelli",
                'description': 'test description',
                'location': 'Torino'}

        tool.add(**data)
        new_data = {'location': '',
                    'fullname': 'Mario Rossi',
                    }
        data.update(new_data)
        tool.update(**data)

        # updating user without location it will be removed from tool
        ud = tool.get(data['userid'])
        self.assertIsNone(ud)

    def test_add_user_without_location(self):
        tool = UsersCoordinates(id='portal_userscoordinates')
        data = {'userid': 'giorgio',
                'fullname': "Giorgio Borelli",
                'description': 'test description',
                'location': ''}
        tool.add(**data)
        ud = tool.get(data['userid'])
        self.assertIsNone(ud)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUtility))
    return suite
