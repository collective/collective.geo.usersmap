from zope.interface import implements
from plone.app.users.userdataschema import IUserDataSchemaProvider
from collective.geo.usermap.interfaces import IEnhancedUserDataSchema


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        return IEnhancedUserDataSchema
