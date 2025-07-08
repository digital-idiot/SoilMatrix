Getting Started
======================================

Welcome to the full project guide.

This page provides detailed instructions on setting up and using the project locally.

Create the Repository
---------------------
Navigate to the template you want to use on GitHub, and click the "Use this template" button to create a new repository. Follow the prompts to name your repository and choose its visibility (public or private).

Clone the Repository
--------------------

.. code-block:: bash

   git clone https://github.com/systemiqofficial/your-project.git
   cd your-project

Create and Activate a Virtual Environment
------------------------------------------

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

Install Dependencies
---------------------

.. code-block:: bash

   pip install -r requirements.txt


Set Up Environment Variables
----------------------------

If your project uses a `.env` file:

.. code-block:: bash

   cp .env_template .env

Then edit `.env` to add your own keys or configurations.

Running Tests
-------------

We use `pytest` for running unit tests:

.. code-block:: bash

   pytest

Documentation 
---------------------------

This project uses `Sphinx` for documentation. See :ref:`documentation-label` for more details.

To build the docs locally:

.. code-block:: bash

   cd docs
   make html