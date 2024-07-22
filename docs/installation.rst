Installation
============

There are two main ways to install SquirrelUno: locally from the source code or directly from GitHub.

Local Installation
==================

To install the package locally from the source code, follow these steps:

1. **Clone the repository**:

    First, clone the SquirrelUno repository to your local machine using the following command:

    .. code-block:: bash

       git clone https://github.com/MarvGMBH/SquirrelUno.git
       cd SquirrelUno

2. **Create a virtual environment (optional but recommended)**:

    It is recommended to create a virtual environment to avoid conflicts with other packages. You can create and activate a virtual environment using the following commands:

    .. code-block:: bash

       python -m venv venv
       source venv/bin/activate   # On Windows use `venv\Scripts\activate`

3. **Install the package in editable mode**:

    Install the package in editable mode so you can make changes to the source code and have them reflected immediately. Use the following command:

    .. code-block:: bash

       pip install -e .

4. **Verify the installation**:

    To verify that the installation was successful, run the following command:

    .. code-block:: bash

       python -m uno --version

    You should see the version information printed on the screen.

GitHub Installation
===================

To install the package directly from GitHub without cloning the repository, run:

.. code-block:: bash

   pip install git+https://github.com/MarvGMBH/SquirrelUno.git

This command will fetch the latest version of SquirrelUno from the GitHub repository and install it on your machine.

### Notes

- **Dependencies**: All required dependencies will be installed automatically when you install the package.
- **Updates**: To update the package, you can pull the latest changes from the repository and reinstall it in editable mode, or if installed directly from GitHub, simply run the installation command again.

Verifying the Installation
==========================

After installation, you can verify that everything is set up correctly by running:

.. code-block:: bash

   python -m uno --help

You should see a help message describing the available commands and options for SquirrelUno.
