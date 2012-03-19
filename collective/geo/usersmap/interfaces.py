from zope import schema
from zope.interface import Interface
from zope.interface import Attribute
from plone.theme.interfaces import IDefaultPloneLayer
from collective.geo.usersmap import _


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IUsersMapView(Interface):
    """Marker interface for UsersMapView
    """


class IUsersMapPreferences(Interface):
    """Users Map settings for plone.app.registry
    """
    title = schema.TextLine(title=_(u"Map Title"))
    description = schema.Text(title=_(u"Map Description"))
    user_properties = schema.List(
        title=_(u'Profile properties'),
        description=_(u"Add users' properties, one for line. " \
                    "They will be displayed in the map popups"),
        value_type=schema.TextLine(title=_(u"Property")),
        required=False,
    )


class IUsersCoordinates(Interface):
    """Marker interface to UsersCoortinate utility
    """


class IUserDescription(Interface):
    """Adapter used to compose the baloon of the users' map
    """

    user_props = Attribute("User properties to use in description")

    def get_description(self, userid, usr_data):
        """Return a description in html format
        """
