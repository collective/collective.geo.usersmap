# -*- coding: utf-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting


class UsersMapFixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # pylint: disable=W0613
        import collective.geo.usersmap
        self.loadZCML(package=collective.geo.usersmap)
        self.loadZCML(name="overrides.zcml",
                    package=collective.geo.usersmap.tests)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.geo.usersmap:default')


BASE_FIXTURE = UsersMapFixture()

INTEGRATION_TESTING = IntegrationTesting(
                                    bases=(BASE_FIXTURE, ),
                                    name="UsersMapFixture:Integration")

FUNCTIONAL_TESTING = FunctionalTesting(
                                    bases=(BASE_FIXTURE, ),
                                    name="UsersMapFixture:Functional")
