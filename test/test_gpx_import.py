import pytest
import os

from utils.gpx_import import GpxImport


@pytest.fixture(scope="module")
def imported_gpx():
    filename = os.path.join("test", "data", "20200621_Granite_Mountain.GPX")
    return GpxImport(filename=filename)


def test_name(imported_gpx):
    assert imported_gpx.name == "20200621_Granite_Mountain.GPX"


def test_coordinates_count(imported_gpx):
    assert len(imported_gpx.coordinates) == 6875
    assert len(imported_gpx.coordinates) == imported_gpx.segment.point_count


def test_invalid_file():
    filename = os.path.join("test", "data", "invalid.GPX")
    with pytest.raises(Exception):
        GpxImport(filename=filename)
