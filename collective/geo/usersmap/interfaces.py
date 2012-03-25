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


class IUserData(Interface):
    """UserData mapping used on IUserCoordinates registry
    """


class IUsersCoordinates(Interface):
    """Marker interface for UsersCoortinates registry
    """

    geocoder = Attribute("Return a geocoder utility")

    def records(self):
        """Return an OOBTree of IUserData
        """

    def items(self):
        """Return a list of IUsersCoordinates's
        (userid, IUserData) pairs, as 2-tuples
        """

    def iteritems(self):
        """Return an iterator over the (userid, IUserData) items of
        IUsersCoordinates
        """

    def keys(self):
        """Return a list of userid registered on IUsersCoordinates
        """

    def get(self, name, default=None):
        """Return a IUserData by userid
        """

    def add(self, userid, location, fullname, description):
        """Add IUserData to registry
        """

    def update(self, userid, location, fullname, description):
        """Update IUserData of existing userid.
        Without providing location attribute the user
        will be removed from registry
        """

    def delete(self, userid):
        """Delete IUserData from registry by userid
        """

    def get_coordinates(self, location):
        """Retrive coordinates with IGeoCoder and return
        the first coordinates retrieved
        """
