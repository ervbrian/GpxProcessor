import pytest


@pytest.mark.usefixtures("segment")
def test_segment_distance_calculation(segment):
    assert segment.distance == 13.12880768852734


@pytest.mark.usefixtures("segment")
def test_segment_speed_calculation(segment):
    assert segment.speed == 10.23


@pytest.mark.usefixtures("segment")
def test_segment_elevation_calculation(segment):
    assert segment.ascent == 500
    assert segment.descent == -300


@pytest.mark.usefixtures("segment")
def test_segment_duration_calculation(segment):
    assert segment.duration == 77


@pytest.mark.usefixtures("segment")
def test_segment_ascent_rate_calculation(segment):
    assert segment.ascent_rate == 500


@pytest.mark.usefixtures("segment")
def test_segment_heart_rate_calculation(segment):
    assert segment.average_heart_rate == 158


@pytest.mark.usefixtures("hike")
def test_hike_distance_calculation(hike):
    assert hike.distance == 65.64


@pytest.mark.usefixtures("hike")
def test_hike_elevation_calculation(hike):
    assert hike.ascent == 2500
    assert hike.descent == -1500


@pytest.mark.usefixtures("hike")
def test_hike_duration_calculation(hike):
    assert hike.duration == 385


@pytest.mark.usefixtures("hike")
def test_hike_speed_calculation(hike):
    assert hike.speed == 10.23


@pytest.mark.usefixtures("hike")
def test_hike_ascent_rate_calculation(hike):
    assert hike.ascent_rate == 500


@pytest.mark.usefixtures("hike")
def test_hike_heart_rate_calculation(hike):
    assert hike.average_heart_rate == 158
