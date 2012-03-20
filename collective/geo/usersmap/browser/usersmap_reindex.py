from zope.component import getUtility

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from ..interfaces import IUsersCoordinates
from ..interfaces import IUserDescription


class Reindex(BrowserView):

    def _reindex(self):
        userscoords = getUtility(IUsersCoordinates)
        user_desc_adpt = IUserDescription(self.context)
        usr_props = ['fullname', 'location']

        memberdata_tool = getToolByName(self.context, 'portal_memberdata')
        properties = memberdata_tool.propertyIds()
        membership = getToolByName(self.context, 'portal_membership')

        users = membership.listMemberIds()
        for userid in users:
            data = {}
            member = membership.getMemberById(userid)
            for prop in properties:
                data[prop] = member.getProperty(prop)

            usr_data = {}
            for i in usr_props:
                usr_data[i] = data[i]

            usr_description = user_desc_adpt.get_description(userid, data)
            usr_data['description'] = usr_description

            if userid not in userscoords:
                userscoords.add(userid, **usr_data)
            else:
                userscoords.update(userid, **usr_data)

        return len(users)

    def __call__(self):
        n_users = self._reindex()
        return u'All done - %d users' % n_users
