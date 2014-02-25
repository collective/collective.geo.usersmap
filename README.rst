Introduction
============

This package provides a map showing the registered users of the portal by the location attributes of each user.

How it works
============

The "location" attribute in the user's profile is automatically transformed in its corresponding coordinates, and then registered in a specific utility.

The Plone registry contains keys to manage the title and description showing on the map, and the list of user's attributes to show in the map in the specified order.

How to use the map
==================

This package provides both a browser view at <portal_url>/@@usersmap_view and a portlet named "usersmap portlet".

Utils
=====

A browser view at <portal_url>/@@usersmap_reindex is provided to let the admin reindex all the users' locations in case of any misalignment.

Known bugs
==========

You can set just one "usersmap portlet" per page.

Dependencies
============

* Plone >= 4.2
* collective.geo.mapwidget > 2.0

Contributors
============

* Giorgio Borelli - gborelli
* Leonardo J. Caballero G. - macagua
