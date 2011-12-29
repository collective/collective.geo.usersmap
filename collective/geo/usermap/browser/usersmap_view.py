from time import time

from zope.interface import implements
from zope.component import getUtility
from Products.Five import BrowserView
from Products.CMFPlone.utils import getToolByName

from plone.memoize import ram
from plone.registry.interfaces import IRegistry
from collective.geo.geographer.interfaces import IGeoCoder

from ..interfaces import IUsersMapView
from ..interfaces import IUserMapPreferences
from ..utils import coordinate_transform


DESC_TEMPLATE = """<![CDATA[<div
class='user-description'
dir="ltr">%s</div>]]>
"""


class UserMapMixin(BrowserView):

    @property
    def portal_registry(self):
        return getUtility(IRegistry)

    @property
    def usermap_config(self):
        return self.portal_registry.forInterface(IUserMapPreferences)

    @property
    def title(self):
        return self.usermap_config.title

    @property
    def description(self):
        return self.usermap_config.description


class UsersMapView(UserMapMixin):
    """Kml Users Map View
    """
    implements(IUsersMapView)


class UsersMapKMLView(UserMapMixin):

    _user_properties = ['fullname', 'description']

    @property
    def description(self):
        return "<![CDATA[%s]]>" % self.usermap_config.description

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
        users = []
        for memberId in membership.listMemberIds():
            member = membership.getMemberById(memberId)
            location = member.getProperty('location')
            if not location:
                continue

            geo_data = self.geocoder.retrieve(location)
            if not geo_data:
                continue

            latitude, longitude = coordinate_transform(
                                        geo_data[0][1],
                                        unique_coordinate)
            user = {'location':
                        "%r,%r,0.000000" % (longitude, latitude)}
            for prop in self._user_properties:
                if prop == 'description':
                    user[prop] = DESC_TEMPLATE % \
                                 member.getProperty(prop)
                else:
                    user[prop] = member.getProperty(prop)
            # yield user -- doesn't work with memoize
            users.append(user)
        return users
