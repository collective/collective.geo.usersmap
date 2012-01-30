from zope import schema
from zope.interface import Interface
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


class IUsersCoordinates(Interface):
    """Marker interface to UsersCoortinate utility
    """
