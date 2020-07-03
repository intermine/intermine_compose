Intermine Compose
==============================

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference

Installation
------------

To install intermine_compose,
run this command in your terminal at the root of this project:

.. code-block:: console

   $ poetry install


Usage
-----

intermine_compose usage looks like:

.. code-block:: console

   $ intermine_compose [Command] [Flags]

**Commands**

.. option:: run

   Runs the backend server in debug mode.

.. warning:: Do not use this in prodcution.

.. option:: db [Command] [Flags]

   Runs database management related operations.

   **Commands**

   .. option:: init

   Initializes the database.

   .. option:: destroy

   Drops all the database tables.

   .. option:: reset

   Drops all the database tables and then recreates them.

**Flags**

.. option:: --help

   Display a short usage message and exit.
