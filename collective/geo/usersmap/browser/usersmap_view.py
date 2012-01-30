from time import time

from zope.interface import implements
from zope.component import getUtility
from Products.Five import BrowserView

from plone.memoize import ram
from plone.registry.interfaces import IRegistry

from ..interfaces import IUsersMapView
from ..interfaces import IUsersMapPreferences
from ..interfaces import IUserCoordinates
from ..utils import coordinate_transform


DESC_TEMPLATE = """<![CDATA[<div
class='user-description'
dir="ltr">%s</div>]]>
"""


class UsersMapMixin(BrowserView):

    @property
    def portal_registry(self):
        return getUtility(IRegistry)

    @property
    def usersmap_config(self):
        return self.portal_registry.forInterface(IUsersMapPreferences)

    @property
    def title(self):
        return self.usersmap_config.title

    @property
    def description(self):
        return self.usersmap_config.description


class UsersMapView(UsersMapMixin):
    """Kml Users Map View
    """
    implements(IUsersMapView)


class UsersMapKMLView(UsersMapMixin):

    _user_properties = ['fullname', 'description']

    @property
    def description(self):
        return "<![CDATA[%s]]>" % self.usersmap_config.description

    @property
    def user_coords_tool(self):
        return getUtility(IUserCoordinates)

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
        unique_coordinate = []
        users = []
        for user_id in self.user_coords_tool:
            member_data = self.user_coords_tool.get(user_id)
            latitude, longitude = coordinate_transform(
                                        member_data.get('coordinates'),
                                        unique_coordinate)
            user = {'location':
                        "%r,%r,0.000000" % (longitude, latitude)}

            for prop in self._user_properties:
                if prop == 'description':
                    user[prop] = DESC_TEMPLATE % \
                                 member_data.get(prop, '')
                else:
                    user[prop] = member_data.get(prop, '')
            # yield user -- doesn't work with memoize
            users.append(user)

        return users
