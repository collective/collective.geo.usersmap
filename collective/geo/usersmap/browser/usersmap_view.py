from time import time

from zope.interface import implements
from zope.component import getUtility
from Products.Five import BrowserView

from plone.memoize import ram
from plone.registry.interfaces import IRegistry

from collective.geo.mapwidget.browser import widget

from ..interfaces import IUsersMapView
from ..interfaces import IUsersMapPreferences
from ..interfaces import IUsersCoordinates
from ..utils import coordinate_transform


DESC_TEMPLATE = """<![CDATA[<div
class='user-description'
dir="ltr">%s</div>]]>
"""


class MapWidget(widget.MapWidget):
    js = None

    @property
    def mapid(self):
        return "usersmap-view"


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

    @property
    def cgmap(self):
        return MapWidget(self, self.request, self.context)

    def __init__(self, context, request):
        super(UsersMapView, self).__init__(context, request)
        self.request.set('disable_border', True)


class UsersMapKMLView(UsersMapMixin):

    _user_properties = ['fullname', 'description']

    @property
    def description(self):
        return "<![CDATA[%s]]>" % self.usersmap_config.description

    @property
    def user_coords_tool(self):
        return getUtility(IUsersCoordinates)

    # caching for two hours (?)
    # @ram.cache(lambda *args: time() // (120 * 60))
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
                    desc = member_data.get(prop) or ''
                    user[prop] = DESC_TEMPLATE % desc
                else:
                    user[prop] = member_data.get(prop, '')
            # yield user -- doesn't work with memoize
            users.append(user)

        return users
