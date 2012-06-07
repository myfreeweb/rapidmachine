Installation
============

RapidMachine requires Python 2.5 or newer, but it's not compatible with Python 3.

Installing a released version
-----------------------------

You can install RapidMachine with `pip`_::

    $ pip install rapidmachine

You should use `virtualenv`_ for your projects.
If you really want to install RapidMachine globally, you probably need sudo::

    $ sudo pip install rapidmachine

On Python 2.5, you also have to install `simplejson`_.

Installing master from Git
--------------------------

You can install the current development snapshot from `git`_::

    $ git clone git://github.com/myfreeweb/rapidmachine
    $ cd rapidmachine
    $ sudo python setup.py install


.. _pip: http://www.pip-installer.org/en/latest/index.html
.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _git: http://git-scm.org
.. _simplejson: http://simplejson.readthedocs.org
