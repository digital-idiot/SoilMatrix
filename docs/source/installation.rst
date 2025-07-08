Installation
============

Using pip
---------

You can install SoilMatrix directly from GitHub using pip:

.. code-block:: bash

    pip install git+https://github.com/digital-idiot/SoilMatrix.git

For development installation, you can clone the repository and install in development mode:

.. code-block:: bash

    git clone https://github.com/digital-idiot/SoilMatrix.git
    cd SoilMatrix
    pip install -e .

Dependencies
------------

SoilMatrix has the following core dependencies:

- Python 3.10+
- geopandas >= 0.14.0
- numpy >= 1.24.0
- rasterio >= 1.3.0
- requests >= 2.31.0
- tqdm >= 4.66.0

These will be automatically installed when you install SoilMatrix using pip.
