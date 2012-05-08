from zope.component import getUtility

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from ..interfaces import IUsersCoordinates
from ..interfaces import IUserDescription


class Reindex(BrowserView):

    @property
    def userscoords(self):
        return getUtility(IUsersCoordinates)

    def _reindex(self):
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

            if userid not in self.userscoords:
                self.userscoords.add(userid, **usr_data)
            else:
                self.userscoords.update(userid, **usr_data)

        return len(users)

    def _purge_orphan_users(self):
        membership = getToolByName(self.context, 'portal_membership')
        user_ids = membership.listMemberIds()
        n_orphan = 0
        for _id in list(self.userscoords.keys()):
            if _id not in user_ids:
                self.userscoords.delete(_id)
                n_orphan += 1
        return n_orphan

    def __call__(self):
        n_users = self._reindex()
        n_orphan = self._purge_orphan_users()
        return u'All done - updated %d users and ' \
            u'removed %d users' % (n_users, n_orphan)
