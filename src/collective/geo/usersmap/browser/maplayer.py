from plone.memoize.instance import memoizedproperty
from collective.geo.mapwidget.maplayers import MapLayer
from collective.geo.mapwidget.browser.widget import MapLayers


class KMLMapLayer(MapLayer):
    """map layer see: collective.geo.mapwidget
    """
    name = 'usersmap'

    @memoizedproperty
    def jsfactory(self):
        title = self.context.Title().replace("'", "\'")
        if isinstance(title, str):
            title = title.decode('utf-8')
        plone_view = self.context.restrictedTraverse('plone_portal_state')
        plone_url = plone_view.portal_url()
        if not plone_url.endswith('/'):
            plone_url += '/'
        template = self.context.restrictedTraverse('%s-layer' % self.name)()
        return template % (title,
                           plone_url)


class KMLMapLayers(MapLayers):
    """Create all layers for IUsersMapView.
    """

    def layers(self):
        layers = super(KMLMapLayers, self).layers()
        layers.append(KMLMapLayer(context=self.context))
        return layers
