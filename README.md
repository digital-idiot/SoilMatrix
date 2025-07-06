# 🌱 SoilMatrix

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/soilmatrix)](https://pypi.org/project/soilmatrix/)

A Python package for fetching and processing soil data from the SoilGrids API. SoilMatrix provides an easy-to-use interface to access global soil property and class maps at different depths.

## 📋 Features

- Fetch soil property data at different depths including bulk density, clay content, sand content, and more
- Get data for a specific area of interest.
- Get data in any desired projection.
- Shows progress in CLI of the download.

## 🔄 TODO
- Deriving USDA Soil Texture
- Providing callback for progress

## 🚀 Installation

### Using pip

```bash
pip install git+git@github.com:digital-idiot/SoilMatrix.git
```

## 🛠️ Usage

### Basic Usage

```python
from soilmatrix import SoilMatrix
import geopandas as gpd

# Create a GeoDataFrame with your area of interest
geo_array = gpd.points_from_xy(
    x=[-1.550],
    y=[5.358],
    crs="EPSG:4326"
)  # A point in Ghana Cocoa Belt

# Take 5km buffer as the area of interest
geo_array = geo_array.to_crs("EPSG:3857").buffer(5000).to_crs("EPSG:4326")

# Initialize SoilMatrix
soil = SoilMatrix()

# Fetch clay content for the given AOI
soil.get_soildata(
    gdf=geo_array,
    service_id="clay",
    coverage_id="5-15cm_mean",
    aoi=geo_array,
    dst_path="",
    convert=True,
    all_touched=False,
    invert=False,
    block_height=256,
    block_width=256,
    show_progress=True,
    transient_progress=False,
    resampling="nearest",
    dst_opts={
        "crs": "EPSG:8857",
        "driver": "COG",
        "compress": "ZSTD",
        "LEVEL": 11,
        "NUM_THREADS": "ALL_CPUS",
        "PREDICTOR": "YES",
        "BIGTIFF": "IF_SAFER",
        "RESAMPLING": "NEAREST",
        "OVERVIEW_RESAMPLING": "NEAREST",
        "WARP_RESAMPLING": "NEAREST",
        "OVERVIEWS": "IGNORE_EXISTING",
        "OVERVIEW_COUNT": 2,
        "OVERVIEW_COMPRESS": "ZSTD",
        "OVERVIEW_PREDICTOR": "YES",
        "SPARSE_OK": "TRUE",
        "STATISTICS": "FALSE",
        "BLOCKSIZE": 256
    }
)
```

### Available Soil Properties

- `bdod`: Bulk density of the fine earth fraction (cg/cm³)
- `cec`: Cation Exchange Capacity of the soil (mmol(c)/kg)
- `cfvo`: Volumetric fraction of coarse fragments (cm³/dm³)
- `clay`: Proportion of clay particles (g/kg)
- `nitrogen`: Total nitrogen (cg/kg)
- `phh2o`: Soil pH in H₂O
- `sand`: Proportion of sand particles (g/kg)
- `silt`: Proportion of silt particles (g/kg)
- `soc`: Soil organic carbon content (dg/kg)
- `ocd`: Organic carbon density (hg/m³)
- `ocs`: Organic carbon stocks (t/ha)
- `wrb`: World Reference Base (WRB) soil classification

## 📖 Documentation

For detailed documentation, including API reference and examples, please visit [the documentation site](https://digital-idiot.github.io/SoilMatrix/).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ISRIC - World Soil Information](https://www.isric.org/) for providing the SoilGrids data
- All contributors who have helped improve this project

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/digital-idiot">digital-idiot</a>
</div>
