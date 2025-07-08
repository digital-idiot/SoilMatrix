Contributing
============

We welcome contributions to SoilMatrix! Here's how you can help:

1. **Report Bugs**: If you find a bug, please open an issue on `GitHub <https://github.com/digital-idiot/SoilMatrix/issues>`_ with a clear description and steps to reproduce.

2. **Fix Bugs**: Check the `GitHub issues <https://github.com/digital-idiot/SoilMatrix/issues>`_ for bugs that need fixing.

3. **Add Features**: Have an idea for a new feature? Open an issue first to discuss it with the maintainers.

4. **Improve Documentation**: Good documentation is crucial. Help us improve it!

Development Setup
-----------------

1. Fork the repository on GitHub
2. Clone your fork locally:

   .. code-block:: bash

       git clone git@github.com:your-username/SoilMatrix.git
       cd SoilMatrix

3. Create a virtual environment and activate it:

   .. code-block:: bash

       python -m venv venv
       source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install the package in development mode with all dependencies:

   .. code-block:: bash

       pip install -e ".[dev]"
       pre-commit install

5. Create a branch for your changes:

   .. code-block:: bash

       git checkout -b feature/your-feature-name

6. Make your changes and run the tests:

   .. code-block:: bash

       pytest

7. Commit your changes with a descriptive commit message:

   .. code-block:: bash

       git commit -am "Add some feature"

8. Push your branch and open a pull request

Coding Standards
----------------

- Follow `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ style guide
- Use type hints for all new code
- Write docstrings following the Google style guide
- Include tests for new features
- Update documentation when adding new features

Running Tests
-------------

Run the test suite with:

.. code-block:: bash

    pytest

Or with coverage:

.. code-block:: bash

    pytest --cov=soilmatrix tests/

Code of Conduct
---------------

This project adheres to the Contributor Covenant `code of conduct <https://www.contributor-covenant.org/version/2/1/code_of_conduct/>`_. By participating, you are expected to uphold this code.
