from zope.component import getUtility

from Products.CMFCore.utils import getToolByName
from plone.app.users.browser.interfaces import IAccountPanelForm

from interfaces import IUsersCoordinates
from interfaces import IUserDescription


def notify_user_preferences_changed(event):
    """Insert or Update user data in IUsersCoordinates tool
    """
    context = event.context
    form_data = event.data
    userid = getattr(context, 'userid', None)

    props = ['fullname', 'location']

    if not IAccountPanelForm.providedBy(context):
        return

    for i in props:
        if i not in form_data.keys():
            return

    if not userid:
        mt = getToolByName(context, 'portal_membership')
        userid = mt.getAuthenticatedMember().id

    tool = getUtility(IUsersCoordinates)
    data = {}
    for el in props:
        data[el] = form_data.get(el, '')

    user_desc = IUserDescription(context)
    data['description'] = user_desc.get_description(userid, form_data)

    if userid not in tool:
        tool.add(userid, **data)
    else:
        tool.update(userid, **data)
