from plone.app.users.browser.interfaces import IAccountPanelForm
from zope.component import getUtility
from interfaces import IUserCoordinates


def notify_user_preferences_changed(event):
    """Insert or Update user data in IUserCoordinates tool
    """
    context = event.context
    form_data = event.data
    userid = getattr(context, 'userid', None)
    if not IAccountPanelForm.providedBy(context) or \
        not userid:
        return

    tool = getUtility(IUserCoordinates)
    props = ['fullname', 'location']
    data = {}
    for el in props:
        data[el] = form_data.get(el, '')

    if userid not in tool:
        tool.add(userid, **data)
    else:
        tool.update(userid, **data)
