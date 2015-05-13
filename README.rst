***************************
Greylist Server for Postfix
***************************

|Build Status| |health| |docs| |pypi downloads| |pypi version| |pypi licence| |pypi wheel| |requires status|

Features
********

- Greylist Server high performance
- Backends: MongoDB, PostgreSQL, MySQL, Sqlite
- Configuration by ip address & cidr, sender, recipient, ... (and by regex)
- WebUI (optional)
- White and Black lists
- Anti-relaying and anti-spoofing controls
- REST Api (in progress)
- Cache with Memory or Redis

* `Documentation Française <http://mongrey.readthedocs.org/fr/latest/>`_

Contributing
************

To contribute to the project, fork it on GitHub and send a pull request, all contributions and suggestions are welcome.

.. _MongoDB: http://mongodb.org/
.. _Docker: https://www.docker.com/
.. _Ubuntu: http://www.ubuntu.com/
.. _Dockerfile: http://dockerfile.github.io/#/mongodb
.. _Python: http://www.python.org/
.. _Gevent: http://www.gevent.org/
.. _Postfix: http://www.postfix.org
.. _Postfix_Policy: http://www.postfix.org/SMTPD_POLICY_README.html
.. _Coroutine: http://en.wikipedia.org/wiki/Coroutine
 
.. |Build Status| image:: https://travis-ci.org/radical-software/mongrey.svg?branch=master
   :target: https://travis-ci.org/radical-software/mongrey
   :alt: Travis Build Status
   
.. |pypi downloads| image:: https://img.shields.io/pypi/dm/mongrey.svg
    :target: https://pypi.python.org/pypi/mongrey
    :alt: Number of PyPI downloads
    
.. |pypi version| image:: https://img.shields.io/pypi/v/mongrey.svg
    :target: https://pypi.python.org/pypi/mongrey
    :alt: Latest Version

.. |pypi licence| image:: https://img.shields.io/pypi/l/mongrey.svg
    :target: https://pypi.python.org/pypi/mongrey
    :alt: License

.. |pypi wheel| image:: https://pypip.in/wheel/mongrey/badge.png
    :target: https://pypi.python.org/pypi/mongrey/
    :alt: Python Wheel
        
.. |requires status| image:: https://requires.io/github/radical-software/mongrey/requirements.svg?branch=master
     :target: https://requires.io/github/radical-software/mongrey/requirements/?branch=master
     :alt: Requirements Status

.. |docs| image:: https://readthedocs.org/projects/mongrey-en/badge/?version=latest
    :target: http://mongrey.readthedocs.org/en/latest/
    :alt: Documentation Status     
    
.. |health| image:: https://landscape.io/github/radical-software/mongrey/master/landscape.svg?style=flat
   :target: https://landscape.io/github/radical-software/mongrey/master
   :alt: Code Health
