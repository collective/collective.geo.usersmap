from zope import schema
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IUsersMapView(Interface):
    """Marker interface for UsersMapView
    """


class IUserMapPreferences(Interface):
    """Users Map settings for plone.app.registry
    """
    title = schema.TextLine(title=u"Map Title")
    description = schema.Text(title=u"Map Description")
