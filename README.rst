Introduction
============

``collective.geo.usersmap`` provides a map showing the registered users of 
the portal by the location attributes of each user.

How it works
============

The "location" attribute in the user's profile is automatically transformed 
in its corresponding coordinates, and then registered in a specific utility.

The Plone registry contains keys to manage the title and description showing 
on the map, and the list of user's attributes to show in the map in the 
specified order.

How to use the map
==================

``collective.geo.usersmap`` provides both a browser view at ``<portal_url>/@@usersmap_view`` 
and a portlet named "usersmap portlet".

Utils
=====

A browser view at <portal_url>/@@usersmap_reindex is provided to let the admin 
reindex all the users' locations in case of any misalignment.

Known bugs
==========

You can set just one "usersmap portlet" per page.

Dependencies
============

* `Plone`_ >= 4.2
* `collective.geo.mapwidget`_ > 2.0


Documentation
=============

Full documentation for end users can be found in the "docs" folder.
It is also available online at https://collectivegeo.readthedocs.io/


Translations
============

This product has been translated into

- Spanish.

- Italian.

You can contribute for any message missing or other new languages, join us at 
`Plone Collective Team <https://www.transifex.com/plone/plone-collective/>`_ 
into *Transifex.net* service with all world Plone translators community.


Installation
============

This addon can be installed has any other addons, please follow official
documentation_.


Tests status
============

This add-on is tested using Travis CI. The current status of the add-on is:

.. image:: https://img.shields.io/travis/collective/collective.geo.usersmap/master.svg
    :target: https://travis-ci.org/collective/collective.geo.usersmap

.. image:: http://img.shields.io/pypi/v/collective.geo.usersmap.svg
   :target: https://pypi.org/project/collective.geo.usersmap


Contribute
==========

Have an idea? Found a bug? Let us know by `opening a ticket`_.

- Issue Tracker: https://github.com/collective/collective.geo.usersmap/issues
- Source Code: https://github.com/collective/collective.geo.usersmap
- Documentation: https://collectivegeo.readthedocs.io/


Contributors
============

* Giorgio Borelli - gborelli
* Leonardo J. Caballero G. - macagua


License
=======

The project is licensed under the GPLv2.


.. _Plone: https://plone.org/
.. _collective.geo.mapwidget: https://pypi.org/project/collective.geo.mapwidget
.. _`opening a ticket`: https://github.com/collective/collective.geo.bundle/issues
.. _documentation: https://docs.plone.org/manage/installing/installing_addons.html

