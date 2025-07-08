Usage
=====

Basic Usage
-----------

Here's a simple example of how to use SoilMatrix to fetch soil data:

.. code-block:: python

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

Available Soil Properties
-------------------------

SoilMatrix supports the following soil properties from SoilGrids:

============= =================================================================
Property      Description
============= =================================================================
bdod          Bulk density of the fine earth fraction (cg/cm³)
cec           Cation Exchange Capacity of the soil (mmol(c)/kg)
cfvo          Volumetric fraction of coarse fragments (cm³/dm³)
clay          Proportion of clay particles (g/kg)
nitrogen      Total nitrogen (cg/kg)
phh2o         Soil pH in H₂O
sand          Proportion of sand particles (g/kg)
silt          Proportion of silt particles (g/kg)
soc           Soil organic carbon content (dg/kg)
ocd           Organic carbon density (hg/m³)
ocs           Organic carbon stocks (t/ha)
wrb           World Reference Base (WRB) soil classification
============= =================================================================

For each property, you can access different depth layers by specifying the appropriate `coverage_id` parameter:

- `0-5cm_mean`
- `5-15cm_mean`
- `15-30cm_mean`
- `30-60cm_mean`
- `60-100cm_mean`
- `100-200cm_mean`

Advanced Usage
--------------

### Customizing Output

You can customize the output format and compression by modifying the `dst_opts` dictionary. The example above shows a typical configuration for Cloud-Optimized GeoTIFF (COG) with ZSTD compression.

### Progress Monitoring

Set `show_progress=True` to display a progress bar during data download and processing. For long-running operations, you can also set `transient_progress=True` to make the progress bar disappear after completion.

### Coordinate Reference Systems (CRS)

SoilMatrix allows you to work with different coordinate reference systems. The example above shows how to transform between WGS84 (EPSG:4326) and Web Mercator (EPSG:3857) for buffering operations. The output CRS can be specified in the `dst_opts` dictionary.
