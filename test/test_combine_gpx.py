import os

from utils.combine_gpx import CombineGpx
from utils.gpx_import import GpxImport
from utils.namespaces import TRK_ELEMENT


file01 = os.path.join("test", "data", "20200619_Snow_Lake.GPX")
file02 = os.path.join("test", "data", "20200619_Snow_Lake_Return.GPX")
output = os.path.join("test", "data", "combined.GPX")
combined = CombineGpx(gpx_files=[file01 ,file02])
combined.write_to_file(filename=output)


def test_combined_trk_count():
    assert len(list(combined.roots[0].findall(TRK_ELEMENT))) == 2


def test_combined_hike_stats():
    combined_import = GpxImport(filename=output)

    assert combined_import.hike.distance == 11.39
    assert combined_import.hike.ascent == 666.4
    assert combined_import.hike.descent == -652.4
    assert combined_import.hike.duration == 289.0
    assert combined_import.hike.ascent_rate == 616.42
    assert combined_import.hike.speed == 2.36
    assert combined_import.hike.average_heart_rate == 118
