from plone.app.users.browser.interfaces import IAccountPanelForm
from zope.component import getUtility
from interfaces import IUsersCoordinates


def notify_user_preferences_changed(event):
    """Insert or Update user data in IUsersCoordinates tool
    """
    context = event.context
    form_data = event.data
    userid = getattr(context, 'userid', None)
    if not IAccountPanelForm.providedBy(context) or \
        not userid:
        return

    tool = getUtility(IUsersCoordinates)
    props = ['fullname', 'location', 'description']
    data = {}
    for el in props:
        data[el] = form_data.get(el, '')

    if userid not in tool:
        tool.add(userid, **data)
    else:
        tool.update(userid, **data)
