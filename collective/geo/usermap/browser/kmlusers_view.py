from zope.interface import implements
from Products.Five import BrowserView
from collective.geo.mapwidget.browser.widget import MapLayers
from maplayer import KMLMapLayer
from ..interfaces import IKMLUsersView


class KmlUsersView(BrowserView):
    """ Kml Users View """

    implements(IKMLUsersView)


class KMLMapLayers(MapLayers):
    """create all layers for this view.
    """

    def layers(self):
        layers = super(KMLMapLayers, self).layers()
        layers.append(KMLMapLayer(context=self.context))
        return layers
