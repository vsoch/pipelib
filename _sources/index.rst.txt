.. _manual-main:

==============
Pipelib Python
==============

.. image:: https://img.shields.io/github/stars/vsoch/pipelib?style=social
    :alt: GitHub stars
    :target: https://github.com/vsoch/pipelib/stargazers


Pipelib is a library for creating pipelines. You can parse, compare, and order iterables. With Pipelib you can:

1. Create a custom pipeline to parse and compare version strings
2. Use a collection of provided sorting functions for custom sorts.
3. Assemble different processing blocks to pre-process inputs first.

The initial ideas came from `Singularity Registry HPC (shpc)` <https://github.com/singularityhub/singularity-hpc/blob/main/shpc/main/container/update/versions.py>`_  that had a need to parse and compare version strings from docker container tags.


.. _main-support:

-------
Support
-------

* For **bugs and feature requests**, please use the `issue tracker <https://github.com/vsoch/pipelib/issues>`_.
* For **contributions**, visit us on `Github <https://github.com/vsoch/pipelib>`_.

---------
Resources
---------

`GitHub Repository <https://github.com/vsoch/pipelib>`_
    The code on GitHub.


.. toctree::
   :caption: Getting started
   :name: getting_started
   :hidden:
   :maxdepth: 3

   getting_started/index
   getting_started/user-guide

.. toctree::
    :caption: API Reference
    :name: api-reference
    :hidden:
    :maxdepth: 1

    api_reference/pipelib
    api_reference/internal/modules
