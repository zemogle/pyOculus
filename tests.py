import pytest

from snapper import rise_set, set_exposure, set_up
from datetime import datetime

class TestCalculations:

    def test_sunset(self):
        now = datetime(2016,4,6,0,10,0)
        sunset = datetime(2016,4,6,18,56)
        sunrise = datetime(2016,4,6,5,2)
        calc_sunset, calc_sunrise = rise_set(now)
        assert sunset == calc_sunset
        assert sunrise == calc_sunrise

# class TestCamera:
#
#     def test_is_camera_attached(self):
