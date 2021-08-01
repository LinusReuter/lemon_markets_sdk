Installation
============

If you first want to try this package, you can do so
`in this colab notebook <https://github.com/>`_. To install it
locally, you have several options. Keep in mind that the minumum
required python version is 3.7:

1. From PyPi (stable versions)
------------------------------

To install a stable version from pypi, use these commands:

**Windows**

.. code-block::

    python -m pip install lemon_markets

**Linux/MacOS**

.. code-block::

    python3 -m pip install lemon_markets


2. From Test-PyPi (prerelease versions)
---------------------------------------

To install a prerelease version from Test-PyPi, use these commands:

**Windows**

.. code-block::

    python -m pip install --index-url https://test.pypi.org/simple/ lemon_markets

**Linux/MacOS**

.. code-block::

    python3 -m pip install --index-url https://test.pypi.org/simple/ lemon_markets


3. Directly from GitHub (bleeding-edge version for contributing)
----------------------------------------------------------------

To install the latest version from GitHub, clone the repository by executing:

.. code-block::

    git clone https://github.com/LinusReuter/lemon-markets-api-access.git

After opening a terminal in this folder, type the following to install the library using
a dynamic link that reflects your latest changes as you make them:

**Windows**

.. code-block::

    python -m pip install -e .

**Linux/MacOS**

.. code-block::

    python3 -m pip install -e .
