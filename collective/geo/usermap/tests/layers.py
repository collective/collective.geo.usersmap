# -*- coding: utf-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting


class UserMapFixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # pylint: disable=W0613
        import collective.geo.usermap
        self.loadZCML(package=collective.geo.usermap)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.geo.usermap:default')


BASE_FIXTURE = UserMapFixture()

INTEGRATION_TESTING = IntegrationTesting(
                                    bases=(BASE_FIXTURE, ),
                                    name="UserMapFixture:Integration")

FUNCTIONAL_TESTING = FunctionalTesting(
                                    bases=(BASE_FIXTURE, ),
                                    name="Fixture:Functional")
