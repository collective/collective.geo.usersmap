from zope.interface import implements
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName

from plone.registry.interfaces import IRegistry

from interfaces import IUserDescription
from interfaces import IUsersMapPreferences


class UserDescription(object):
    implements(IUserDescription)

    def __init__(self, context):
        self.context = context

    def _decode_str(self, data):
        if isinstance(data, basestring) and \
                            not isinstance(data, unicode):
            data = data.decode('utf8')
        return data

    def _default_formatter(self, data):
        return u'<p>%s</p>' % self._decode_str(data)

    def _format_email(self, data):
        data = self._decode_str(data)
        return u'<p><a href="mailto:%s">%s</a></p>' % (data, data)

    def _format_home_page(self, data):
        data = self._decode_str(data)
        return u'<p><a href="%s">%s</a></p>' % (data, data)

    def _format_portrait(self, user_id):
        mtool = getToolByName(self.context, 'portal_membership')
        portrait = mtool.getPersonalPortrait(user_id)
        if portrait.getId() == 'defaultUser.png':
            return None
        return u"<img src='%s' class='map-portrait-photo' />" % \
                                            portrait.absolute_url()

    @property
    def user_props(self):
        registry = getUtility(IRegistry)
        map_preferences = registry.forInterface(IUsersMapPreferences)
        return map_preferences.user_properties

    def get_description(self, user_id, usr_data):
        user_data = []
        for prop in self.user_props:
            data = usr_data.get(prop) or u''
            formatter = getattr(self, '_format_%s' % prop,
                                    self._default_formatter)
            if data:
                user_data.append(formatter(data))
            if prop == 'portrait':
                data = self._format_portrait(user_id)
                if data:
                    user_data.append(data)

        return u'\n'.join(user_data)
