Usage
=====

Running the Project
====================

After installing the package, you can run the main entry point. The command differs slightly between Linux and Windows due to how Python handles module names and entry points on different operating systems.

On Linux
---------

You can run the project using either of the following commands:

.. code-block:: bash

   squirreluno

or

.. code-block:: bash

   python -m uno

On Windows
----------

On Windows, due to certain constraints, you should use the following command:

.. code-block:: bash

   python -m uno

(Note: The `squirreluno` command may not work on Windows due to differences in how Python handles entry points and module names across platforms.)

What You'll See
===============

When you run the project, you should see the following output:

.. code-block:: plaintext

   Welcome to the SquirrelUno project!

Detailed Explanation of Commands
================================

The Uno package provides a command line interface (CLI) that you can use to interact with the project. Here are the details of how you can use the different commands and flags.

Running Without a Command
-------------------------

If you run the project without specifying a command, the default behavior will be executed. For example:

.. code-block:: bash

   python -m uno

This will call the `main` function from the `__init__.py` file. If the `--debug` flag is provided, debugging mode will be enabled:

.. code-block:: bash

   python -m uno --debug

Output:

.. code-block:: plaintext

   Debug Mode active
   Welcome to the SquirrelUno project!

Version Information
-------------------

The CLI provides a command to display version information:

.. code-block:: bash

   python -m uno info

Output:

.. code-block:: plaintext

   v00.xx.xx
   A fun little Uno implementation by Dominik Krenn

If you only want to see the version text and hide additional information, use the `--hide_info` flag:

.. code-block:: bash

   python -m uno info --hide_info

Output:

.. code-block:: plaintext

   v00.xx.xx