"""SoilMatrix Core Module.

Fetch Soil Grids data from the SoilGrids API.
"""
from pathlib import Path
from textwrap import shorten
from typing import Any, ClassVar

import geopandas as gpd
import numpy as np
import rasterio as rio
from rasterio.enums import Resampling
from rasterio.features import geometry_mask, geometry_window
from rasterio.vrt import WarpedVRT
from rasterio.windows import Window, subdivide

from src.utils import ImmutableMeta, TaskProgress

__all__ = ["SoilMatrix"]

class SoilMatrix(metaclass=ImmutableMeta):
    """Main Class: Query & fetch Soil Grids data.

    This is the main class for querying and fetching Soil Grids data.
    """
    DB: ClassVar[dict[str, dict[str, Any]]] = {
        "bdod": {
            "description": "Bulk density of the fine earth fraction",
            "source_unit": "cg/cm³",
            "conversion_factor": 100,
            "target_unit": "kg/dm³",
            "coverages": [
                "0-5cm_Q0.5",
                "0-5cm_Q0.05",
                "0-5cm_Q0.95",
                "0-5cm_mean",
                "0-5cm_uncertainty",
                "5-15cm_Q0.5",
                "5-15cm_Q0.05",
                "5-15cm_Q0.95",
                "5-15cm_mean",
                "5-15cm_uncertainty",
                "15-30cm_Q0.5",
                "15-30cm_Q0.05",
                "15-30cm_Q0.95",
                "15-30cm_mean",
                "15-30cm_uncertainty",
                "30-60cm_Q0.05",
                "30-60cm_Q0.5",
                "30-60cm_Q0.95",
                "30-60cm_mean",
                "30-60cm_uncertainty",
                "60-100cm_Q0.05",
                "60-100cm_Q0.5",
                "60-100cm_Q0.95",
                "60-100cm_mean",
                "60-100cm_uncertainty",
                "100-200cm_Q0.05",
                "100-200cm_Q0.5",
                "100-200cm_Q0.95",
                "100-200cm_mean",
                "100-200cm_uncertainty"
            ]
        },
        "cec": {
            "description": "Cation Exchange Capacity of the soil",
            "source_unit": "mmol(c)/kg",
            "conversion_factor": 10,
            "target_unit": "cmol(c)/kg",
            "coverages": [
                "0-5cm_Q0.05",
                "0-5cm_Q0.5",
                "0-5cm_Q0.95",
                "0-5cm_mean",
                "0-5cm_uncertainty",
                "5-15cm_Q0.05",
                "5-15cm_Q0.5",
                "5-15cm_Q0.95",
                "5-15cm_mean",
                "5-15cm_uncertainty",
                "15-30cm_Q0.5",
                "15-30cm_Q0.05",
                "15-30cm_Q0.95",
                "15-30cm_mean",
                "15-30cm_uncertainty",
                "30-60cm_Q0.05",
                "30-60cm_Q0.5",
                "30-60cm_Q0.95",
                "30-60cm_mean",
                "30-60cm_uncertainty",
                "60-100cm_Q0.5",
                "60-100cm_Q0.05",
                "60-100cm_Q0.95",
                "60-100cm_mean",
                "60-100cm_uncertainty",
                "100-200cm_Q0.5",
                "100-200cm_Q0.05",
                "100-200cm_Q0.95",
                "100-200cm_mean",
                "100-200cm_uncertainty"
            ]
        },
        "cfvo": {
            "description": "Volumetric fraction of coarse fragments (> 2 mm)",
            "source_unit": "cm³/dm³ (vol%)",
            "conversion_factor": 10,
            "target_unit": "cm³/100cm³ (vol%)",
            "coverages": [
                "0-5cm_Q0.05",
                "0-5cm_Q0.5",
                "0-5cm_Q0.95",
                "0-5cm_mean",
                "0-5cm_uncertainty",
                "5-15cm_Q0.5",
                "5-15cm_Q0.05",
                "5-15cm_Q0.95",
                "5-15cm_mean",
                "5-15cm_uncertainty",
                "15-30cm_Q0.5",
                "15-30cm_Q0.05",
                "15-30cm_Q0.95",
                "15-30cm_mean",
                "15-30cm_uncertainty",
                "30-60cm_Q0.5",
                "30-60cm_Q0.05",
                "30-60cm_Q0.95",
                "30-60cm_mean",
                "30-60cm_uncertainty",
                "60-100cm_Q0.05",
                "60-100cm_Q0.5",
                "60-100cm_Q0.95",
                "60-100cm_mean",
                "60-100cm_uncertainty",
                "100-200cm_Q0.05",
                "100-200cm_Q0.5",
                "100-200cm_Q0.95",
                "100-200cm_mean",
                "100-200cm_uncertainty"
            ]
        },
        "clay": {
            "description": "Proportion of clay particles (< 0.002 mm)" +
                           " in the fine earth fraction",
            "source_unit": "g/kg",
            "conversion_factor": 10,
            "target_unit": "g/100g (%)",
            "coverages": [
                "0-5cm_Q0.05",
                "0-5cm_Q0.5",
                "0-5cm_Q0.95",
                "0-5cm_mean",
                "0-5cm_uncertainty",
                "5-15cm_Q0.05",
                "5-15cm_Q0.5",
                "5-15cm_Q0.95",
                "5-15cm_mean",
                "5-15cm_uncertainty",
                "15-30cm_Q0.05",
                "15-30cm_Q0.5",
                "15-30cm_Q0.95",
                "15-30cm_mean",
                "15-30cm_uncertainty",
                "30-60cm_Q0.5",
                "30-60cm_Q0.05",
                "30-60cm_Q0.95",
                "30-60cm_mean",
                "30-60cm_uncertainty",
                "60-100cm_Q0.05",
                "60-100cm_Q0.5",
                "60-100cm_Q0.95",
                "60-100cm_mean",
                "60-100cm_uncertainty",
                "100-200cm_Q0.5",
                "100-200cm_Q0.05",
                "100-200cm_Q0.95",
                "100-200cm_mean",
                "100-200cm_uncertainty"
            ]
        },
        "landmask": {
            "description": "Land Mask",
            "source_unit": None,
            "conversion_factor": None,
            "target_unit": None,
            "coverages": [
                "SG_052020_COG512"
            ]
        },
        "nitrogen": {
            "description": "Total nitrogen (N)",
            "source_unit": "cg/kg",
            "conversion_factor": 100,
            "target_unit": "g/kg",
            "coverages": [
                "0-5cm_Q0.05",
                "0-5cm_Q0.5",
                "0-5cm_Q0.95",
                "0-5cm_mean",
                "0-5cm_uncertainty",
                "5-15cm_Q0.5",
                "5-15cm_Q0.05",
                "5-15cm_Q0.95",
                "5-15cm_mean",
                "5-15cm_uncertainty",
                "15-30cm_Q0.05",
                "15-30cm_Q0.5",
                "15-30cm_Q0.95",
                "15-30cm_mean",
                "15-30cm_uncertainty",
                "30-60cm_Q0.05",
                "30-60cm_Q0.5",
                "30-60cm_Q0.95",
                "30-60cm_mean",
                "30-60cm_uncertainty",
                "60-100cm_Q0.05",
                "60-100cm_Q0.5",
                "60-100cm_Q0.95",
                "60-100cm_mean",
                "60-100cm_uncertainty",
                "100-200cm_Q0.05",
                "100-200cm_Q0.5",
                "100-200cm_Q0.95",
                "100-200cm_mean",
                "100-200cm_uncertainty"
            ]
        },
        "phh2o": {
            "description": "Soil pH",
            "source_unit": "pH x 10",
            "conversion_factor": 10,
            "target_unit": "pH",
            "coverages": [
                "0-5cm_Q0.05",
                "0-5cm_Q0.5",
                "0-5cm_Q0.95",
                "0-5cm_mean",
                "0-5cm_uncertainty",
                "5-15cm_Q0.5",
                "5-15cm_Q0.05",
                "5-15cm_Q0.95",
                "5-15cm_mean",
                "5-15cm_uncertainty",
                "15-30cm_Q0.05",
                "15-30cm_Q0.5",
                "15-30cm_Q0.95",
                "15-30cm_mean",
                "15-30cm_uncertainty",
                "30-60cm_Q0.05",
                "30-60cm_Q0.5",
                "30-60cm_Q0.95",
                "30-60cm_mean",
                "30-60cm_uncertainty",
                "60-100cm_Q0.5",
                "60-100cm_Q0.05",
                "60-100cm_Q0.95",
                "60-100cm_mean",
                "60-100cm_uncertainty",
                "100-200cm_Q0.05",
                "100-200cm_Q0.5",
                "100-200cm_Q0.95",
                "100-200cm_mean",
                "100-200cm_uncertainty"
            ]
        },
        "sand": {
            "description": "Proportion of sand particles (> 0.05/0.063 mm)" +
                           " in the fine earth fraction",
            "source_unit": "g/kg",
            "conversion_factor": 10,
            "target_unit": "g/100g (%)",
            "coverages": [
                "0-5cm_Q0.05",
                "0-5cm_Q0.5",
                "0-5cm_Q0.95",
                "0-5cm_mean",
                "0-5cm_uncertainty",
                "5-15cm_Q0.5",
                "5-15cm_Q0.05",
                "5-15cm_Q0.95",
                "5-15cm_mean",
                "5-15cm_uncertainty",
                "15-30cm_Q0.5",
                "15-30cm_Q0.05",
                "15-30cm_Q0.95",
                "15-30cm_mean",
                "15-30cm_uncertainty",
                "30-60cm_Q0.05",
                "30-60cm_Q0.5",
                "30-60cm_Q0.95",
                "30-60cm_mean",
                "30-60cm_uncertainty",
                "60-100cm_Q0.5",
                "60-100cm_Q0.05",
                "60-100cm_Q0.95",
                "60-100cm_mean",
                "60-100cm_uncertainty",
                "100-200cm_Q0.05",
                "100-200cm_Q0.5",
                "100-200cm_Q0.95",
                "100-200cm_mean",
                "100-200cm_uncertainty"
            ]
        },
        "silt": {
            "description": "Proportion of silt particles" +
                           " (≥ 0.002 mm and ≤ 0.05/0.063 mm) in the fine" +
                           " earth fraction",
            "source_unit": "g/kg",
            "conversion_factor": 10,
            "target_unit": "g/100g (%)",
            "coverages": [
                "0-5cm_Q0.05",
                "0-5cm_Q0.5",
                "0-5cm_Q0.95",
                "0-5cm_mean",
                "0-5cm_uncertainty",
                "5-15cm_Q0.05",
                "5-15cm_Q0.5",
                "5-15cm_Q0.95",
                "5-15cm_mean",
                "5-15cm_uncertainty",
                "15-30cm_Q0.05",
                "15-30cm_Q0.5",
                "15-30cm_Q0.95",
                "15-30cm_mean",
                "15-30cm_uncertainty",
                "30-60cm_Q0.5",
                "30-60cm_Q0.05",
                "30-60cm_Q0.95",
                "30-60cm_mean",
                "30-60cm_uncertainty",
                "60-100cm_Q0.05",
                "60-100cm_Q0.5",
                "60-100cm_Q0.95",
                "60-100cm_mean",
                "60-100cm_uncertainty",
                "100-200cm_Q0.5",
                "100-200cm_Q0.05",
                "100-200cm_Q0.95",
                "100-200cm_mean",
                "100-200cm_uncertainty"
            ]
        },
        "soc": {
            "description": "Soil organic carbon content in the fine" +
                           " earth fraction",
            "source_unit": "dg/kg",
            "conversion_factor": 10,
            "target_unit": "g/kg",
            "coverages": [
                "0-5cm_Q0.5",
                "0-5cm_Q0.05",
                "0-5cm_Q0.95",
                "0-5cm_mean",
                "0-5cm_uncertainty",
                "5-15cm_Q0.05",
                "5-15cm_Q0.5",
                "5-15cm_Q0.95",
                "5-15cm_mean",
                "5-15cm_uncertainty",
                "15-30cm_Q0.5",
                "15-30cm_Q0.05",
                "15-30cm_Q0.95",
                "15-30cm_mean",
                "15-30cm_uncertainty",
                "30-60cm_Q0.05",
                "30-60cm_Q0.5",
                "30-60cm_Q0.95",
                "30-60cm_mean",
                "30-60cm_uncertainty",
                "60-100cm_Q0.05",
                "60-100cm_Q0.5",
                "60-100cm_Q0.95",
                "60-100cm_mean",
                "60-100cm_uncertainty",
                "100-200cm_Q0.05",
                "100-200cm_Q0.5",
                "100-200cm_Q0.95",
                "100-200cm_mean",
                "100-200cm_uncertainty"
            ]
        },
        "ocd": {
            "description": "Organic carbon density",
            "source_unit": "hg/m³",
            "conversion_factor": 10,
            "target_unit": "kg/m³",
            "coverages": [
                "0-5cm_Q0.5",
                "0-5cm_Q0.05",
                "0-5cm_Q0.95",
                "0-5cm_mean",
                "0-5cm_uncertainty",
                "5-15cm_Q0.5",
                "5-15cm_Q0.05",
                "5-15cm_Q0.95",
                "5-15cm_mean",
                "5-15cm_uncertainty",
                "15-30cm_Q0.05",
                "15-30cm_Q0.5",
                "15-30cm_Q0.95",
                "15-30cm_mean",
                "15-30cm_uncertainty",
                "30-60cm_Q0.05",
                "30-60cm_Q0.5",
                "30-60cm_Q0.95",
                "30-60cm_mean",
                "30-60cm_uncertainty",
                "60-100cm_Q0.05",
                "60-100cm_Q0.5",
                "60-100cm_Q0.95",
                "60-100cm_mean",
                "60-100cm_uncertainty",
                "100-200cm_Q0.5",
                "100-200cm_Q0.05",
                "100-200cm_Q0.95",
                "100-200cm_mean",
                "100-200cm_uncertainty"
            ]
        },
        "ocs": {
            "description": "Organic carbon stocks",
            "source_unit": "t/ha",
            "conversion_factor": 10,
            "target_unit": "kg/m²",
            "coverages": [
                "0-30cm_Q0.05",
                "0-30cm_Q0.5",
                "0-30cm_Q0.95",
                "0-30cm_mean",
                "0-30cm_uncertainty"
            ]
        },
        "wrb": {
            "description": "World Reference Base for Soil Resources",
            "source_unit": None,
            "conversion_factor": None,
            "target_unit": None,
            "coverages": [
                "Acrisols",
                "Albeluvisols",
                "Alisols",
                "Andosols",
                "Arenosols",
                "Calcisols",
                "Cambisols",
                "Chernozems",
                "Cryosols",
                "Durisols",
                "Ferralsols",
                "Fluvisols",
                "Gleysols",
                "Gypsisols",
                "Histosols",
                "Kastanozems",
                "Leptosols",
                "Lixisols",
                "Luvisols",
                "MostProbable",
                "Nitisols",
                "Phaeozems",
                "Planosols",
                "Plinthosols",
                "Podzols",
                "Regosols",
                "Solonchaks",
                "Solonetz",
                "Stagnosols",
                "Umbrisols",
                "Vertisols"
            ]
        }
    }

    BASE_URL: ClassVar[str] = "https://files.isric.org/soilgrids/latest/data"

    @property
    def services(self) -> list[str]:
        """List supported services.

        Property to list supported services.

        Returns:
            list[str]: List of service names.
        """
        return list(self.DB.keys())

    @property
    def base_url(self) -> str:
        """Get base URL.

        Property to get the base URL.

        Returns:
            str: The base URL.
        """
        return self.BASE_URL

    def service_exists(self, service_id: str) -> bool:
        """Check service validity.

        Check if a service_id is valid.

        Args:
            service_id (str): The identifier of the service to check.

        Returns:
            bool: True if the service is valid, False otherwise.
        """
        return service_id in self.DB

    def get_coverages(self, service_id: str) -> list[str | Any]:
        """List coverages for a service.

        Get the list of coverages for a given service.

        Args:
            service_id (str): The identifier of the service to get the
             coverages for.

        Returns:
            list[str | Any]: The list of coverages for the service.

        Raises:
            KeyError: If the service_id is not valid.
        """
        if self.service_exists(service_id):
            return self.DB[service_id]["coverages"]
        else:
            raise KeyError(f"Unknown Service: '{service_id}'!")

    def coverage_exists(self, service_id: str, coverage_id: str) -> bool:
        """Check coverage validity.

        Check if a coverage_id is valid for a given service.

        Args:
            service_id (str): The identifier of the service to check.
            coverage_id (str): The identifier of the coverage to check.

        Returns:
            bool: True if the coverage is valid for the service,
             False otherwise.

        Raises:
            KeyError: If the service_id is not valid.
        """
        if self.service_exists(service_id):
            return coverage_id in self.DB[service_id]["coverages"]
        else:
            raise KeyError(f"Unknown Service: '{service_id}'!")

    def source_unit(self, service_id: str) -> str:
        """Get source unit.

        Get the unit of measurement of the values in the source data
         for a given service.

        Args:
            service_id (str): The identifier of the service to get
             the source unit for.

        Returns:
            str: The unit of measurement of the values in the source data.

        Raises:
            KeyError: If the service_id is not valid.
        """
        if self.service_exists(service_id):
            return self.DB[service_id]["source_unit"]
        else:
            raise KeyError(f"Unknown Service: '{service_id}'!")

    def get_conversion_factor(self, service_id: str) -> float:
        """Get conversion factor.

        Get the factor to convert the values from the source unit to
         the target unit for a given service.

        Args:
            service_id (str): The identifier of the service to get the
             conversion factor for.

        Returns:
            float: The conversion factor to convert the values from the source
             unit to the target unit.

        Raises:
            KeyError: If the service_id is not valid.
        """
        if self.service_exists(service_id):
            return self.DB[service_id]["conversion_factor"]
        else:
            raise KeyError(f"Unknown Service: '{service_id}'!")

    def target_unit(self, service_id: str) -> str:
        """Get target unit.

        Get the expected unit of measurement of the values after applying the
         conversion factor for a given service.

        Args:
            service_id (str): The identifier of the service to get the
             target unit for.

        Returns:
            str: The unit of measurement of the values after conversion.

        Raises:
            KeyError: If the service_id is not valid.
        """
        if self.service_exists(service_id):
            return self.DB[service_id]["target_unit"]
        else:
            raise KeyError(f"Unknown Service: '{service_id}'!")

    def get_description(self, service_id: str) -> str:
        """Get service description.

        Retrieve the description for a given service.

        Args:
            service_id (str): The identifier of the service for which to get
             the description.

        Returns:
            str: The description of the specified service.

        Raises:
            KeyError: If the service_id is not valid.
        """
        if self.service_exists(service_id):
            return self.DB[service_id]["description"]
        else:
            raise KeyError(f"Unknown Service: '{service_id}'!")

    def get_url(self, service_id: str, coverage_id: str) -> str:
        """Get source URL.

        Construct the source URL to access a coverage for a given service.

        Args:
            service_id (str): The identifier of the service for which to get
             the coverage URL.
            coverage_id (str): The identifier of the coverage for which to get
             the coverage URL.

        Returns:
            str: The URL to access the specified coverage.

        Raises:
            KeyError: If the specified coverage is not available for the given
             service.
        """
        if self.coverage_exists(service_id, coverage_id):
            if service_id == "wrb":
                return f"{self.base_url}/{service_id}/{coverage_id}.vrt"
            elif service_id == "landmask":
                return f"{self.base_url}/{service_id}/{coverage_id}.tif"
            else:
                return (
                    f"{self.base_url}/{service_id}/" +
                    f"{service_id}_{coverage_id}.vrt"
                )
        else:
            raise KeyError(
                "Unknown Coverage:" +
                f" '{coverage_id}' for Service: '{service_id}'!"
            )

    def get_soildata(
            self,
            service_id: str,
            coverage_id: str,
            aoi: gpd.GeoDataFrame | gpd.GeoSeries,
            dst_path: str | Path,
            convert: bool = False,
            *,
            all_touched: bool = False,
            invert: bool = False,
            block_height: int = 512,
            block_width: int = 512,
            show_progress: bool = True,
            transient_progress: bool = False,
            resampling: str = "nearest",
            dst_opts: dict[str, Any] | None = None
    ) -> None:
        """Ftech coverage.

        Fetch a coverage with specified service clipped to the given AOI
         from the SoilGrids API and save it to disk.

        Args:
            service_id (str): The identifier of the service.
            coverage_id (str): The identifier of the coverage.
            aoi (gpd.GeoDataFrame | gpd.GeoSeries): Vector layer defining
             the area of interest (AOI).
            dst_path (str | Path): The path to save the coverage to.
            convert (bool): If True, convert the data to the target unit.
            all_touched (bool): If True, include all pixels touched by the
             AOI.
            invert (bool): If True, invert the mask so that pixels outside the
             AOI are included.
            block_height (int): The height of the chunk for tiled processing.
            block_width (int): The width of the chunk for tiled processing.
            show_progress (bool): If True, show a progress bar for the task.
            transient_progress (bool): If True, the progress bar will be
             cleared after completion.
            resampling (str): The resampling method to use for reprojection.
            dst_opts (dict[str, Any]): Additional options to pass to the
             rasterio writer.

        Raises:
            KeyError: If the service_id or coverage_id do not exist.
            Exception: If any other error occurs during the operation.
        """
        with TaskProgress(
            disable=not show_progress,
            transient=transient_progress,
            expand=True
        ) as sink:
            task_description = shorten(
                text=f"{service_id}_{coverage_id}", width=32, placeholder="…"
            )
            task = sink.add_task(
                description=task_description,
                total=None,
                stop_status="⚠️"
            )
            try:
                url = self.get_url(
                    service_id=service_id,
                    coverage_id=coverage_id

                )
                pad = 0.5 if all_touched else 0
                with rio.open(url, mode="r") as src_sink:
                    resampling = getattr(
                        Resampling,
                        resampling,  # type: ignore
                        Resampling.nearest
                    )
                    meta = src_sink.meta.copy()
                    if convert:
                        meta["dtype"] = np.float32
                        meta["nodata"] = np.nan
                        unit = self.target_unit(service_id=service_id)
                        conversion_factor = self.get_conversion_factor(
                            service_id=service_id
                        )
                    else:
                        conversion_factor = None
                        unit = self.source_unit(service_id=service_id)
                    if dst_opts:
                        meta |= dst_opts
                    with WarpedVRT(
                        src_dataset=src_sink,
                        crs=meta["crs"],
                        resampling=resampling
                    ) as src:
                        aoi = aoi.to_crs(src.crs).buffer(0) if isinstance(
                            aoi, gpd.GeoSeries
                        ) else aoi.geometry.to_crs(src.crs).buffer(0)
                        shape = aoi.union_all()
                        src_window = geometry_window(
                            dataset=src,
                            shapes=[shape],  # type: ignore
                            pad_x=pad,  # type: ignore
                            pad_y=pad,  # type: ignore
                            boundless=False
                        )
                        src_windows = subdivide(
                            window=src_window,
                            width=block_height,
                            height=block_width
                        )
                        meta["count"]= src.count
                        meta["height"] = src_window.height
                        meta["width"] = src_window.width
                        meta["transform"] = src.window_transform(
                            window=src_window
                        )
                        meta["crs"] = src.crs
                        if meta["nodata"] is None:
                            fill_value = 0
                        else:
                            meta["nodata"] = fill_value = np.dtype(
                                meta["dtype"]
                            ).type(meta["nodata"])
                        with rio.open(dst_path, mode="w", **meta) as dst:
                            sink.update(
                                task_id=task,
                                total=len(src_windows),
                                refresh=True
                            )
                            for swin in src_windows:
                                swin_transform = src.window_transform(
                                    window=swin
                                )
                                dwin = Window(
                                    row_off=(  # type: ignore
                                        swin.row_off - src_window.row_off
                                    ),
                                    col_off=(  # type: ignore
                                        swin.col_off - src_window.col_off
                                    ),
                                    height=swin.height,  # type: ignore
                                    width=swin.width  # type: ignore
                                )
                                mask = geometry_mask(
                                    geometries=[shape],
                                    transform=swin_transform,
                                    out_shape=(swin.height, swin.width),
                                    invert=invert,  # type: ignore
                                    all_touched=all_touched  # type: ignore
                                )
                                if not mask.all():
                                    # noinspection PyTypeChecker
                                    img = src.read(window=swin, masked=True)
                                    img.mask |= np.stack(
                                        ([mask] * meta["count"]),
                                        axis=0
                                    )
                                    img = img.astype(meta["dtype"])
                                    img.fill_value = fill_value
                                    if conversion_factor is not None:
                                        img /= conversion_factor
                                    dst.write(img, window=dwin)
                                else:
                                    dst.write(
                                        np.full(
                                            shape=(
                                                meta["count"],
                                                dwin.height,
                                                dwin.width
                                            ),
                                            fill_value=meta["nodata"],
                                            dtype=meta["dtype"]
                                        ),
                                        window=dwin
                                    )
                                sink.update(
                                    task_id=task,
                                    advance=1,
                                    refresh=True
                                )
                            dst.set_band_description(
                                bidx=1,
                                value=f"{service_id}_{coverage_id}|{unit}"
                            )
            except Exception as exception:
                sink.stop_task(task_id=task)
                raise exception
