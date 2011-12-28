from time import time

from zope.interface import implements
from Products.Five import BrowserView
from Products.CMFPlone.utils import getToolByName

from plone.memoize import ram
from collective.geo.geographer.interfaces import IGeoCoder

from ..interfaces import IUsersMapView
from ..utils import coordinate_transform


class UsersMapView(BrowserView):
    """Kml Users Map View
    """

    implements(IUsersMapView)


class UsersMapKMLView(BrowserView):

    _user_properties = ['fullname', 'description']

    @property
    def geocoder(self):
        return IGeoCoder(self.context)

    # caching for two hours (?)
    @ram.cache(lambda *args: time() // (120 * 60))
    def get_users(self):
        """This function retrieves all Plone user
        and for each user gets the coordinates from its location property.

        Return a list of users which have location property set
        and for which geocoder has retrieved valid coordinates.

        Each element of this list is a dictionary that contains three keys:
        location, fullname, description
        """
        membership = getToolByName(self.context, 'portal_membership')
        unique_coordinate = []
        for memberId in membership.listMemberIds():
            member = membership.getMemberById(memberId)
            location = member.getProperty('location')
            if location:
                geo_data = self.geocoder.retrieve(location)
                if geo_data:
                    latitude, longitude = coordinate_transform(
                                                geo_data[0][1],
                                                unique_coordinate)
                    user = {'location':
                                "%r,%r,0.000000" % (longitude, latitude)}
                    for prop in self._user_properties:
                        user[prop] = member.getProperty(prop)
                    yield user
