from geopy.exc import GeocoderQueryError
from persistent.mapping import PersistentMapping
from OFS.SimpleItem import SimpleItem
from BTrees.OOBTree import OOBTree

from zope.interface import implements
from zope.component import getUtility

from collective.geo.mapwidget.interfaces import IGeoCoder
from collective.geo.usersmap.interfaces import IUsersCoordinates
from collective.geo.usersmap.interfaces import IUserData


class UserData(PersistentMapping):
    """User Data persistent mapping

    This object stores the user's properties used to create
    the kml file which contains the coordinates of users
    """
    implements(IUserData)

    def __init__(self, userid, fullname, description, location, coordinates):
        super(UserData, self).__init__()
        self.update({
            'userid': userid,
            'fullname': fullname,
            'description': description,
            'location': location,
            'coordinates': coordinates,
        })


class UsersCoordinates(SimpleItem):
    implements(IUsersCoordinates)

    def __init__(self, id, title=None):
        super(UsersCoordinates, self).__init__()
        self.id = id
        self.title = title
        self._records = OOBTree()

    @property
    def records(self):
        return self._records

    def __getitem__(self, name):
        return self.records[name]

    def __setitem__(self, name, value):
        if not isinstance(value, UserData):
            raise TypeError
        self.records[name].value = value

    def __contains__(self, name):
        return name in self.records

    def __iter__(self):
        return self.records.__iter__()

    def items(self):
        return self.records.items()

    def iteritems(self):
        return self.records.iteritems()

    def keys(self):
        return self.records.keys()

    def get(self, name, default=None):
        return self.records.get(name, default)

    def add(self, userid, location, fullname, description):
        if userid in self.records:
            raise ValueError

        if not location:
            return None

        coordinates = self.get_coordinates(location)
        if not coordinates:
            return None

        usr_data = UserData(
            userid, fullname,
            description, location, coordinates
        )
        self.records[userid] = usr_data

    def update(self, userid, location, fullname, description):
        if userid in self.records:
            if not location:
                self.delete(userid)
                return None

            coordinates = self.get_coordinates(location)
            if not coordinates:
                return None

            usr_data = self.get(userid)
            usr_data['fullname'] = fullname
            usr_data['description'] = description
            if usr_data['location'] != location:
                usr_data['location'] = location
                usr_data['coordinates'] = coordinates

    def delete(self, userid):
        self.records.pop(userid)

    @property
    def geocoder(self):
        return getUtility(IGeoCoder)

    def get_coordinates(self, location):
        """get coordinates with IGeoCoder and return
        the first coordinates retrieved
        """
        try:
            geo_data = self.geocoder.retrieve(location)
        except GeocoderQueryError:
            return None

        if not geo_data:
            return (0.0, 0.0)
        return geo_data[0][1]
