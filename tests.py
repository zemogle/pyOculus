import pytest
from mock import patch
from snapper import rise_set, set_exposure, setup, DAY_EXP, NIGHT_EXP
from datetime import datetime, timedelta
from astropy.time import Time
import numpy as np

class TestCalculations:

    def test_sunset_sunrise(self):
        brecon = setup()
        now = datetime(2016,4,6,12,10,0)
        sunset = datetime(2016,4,6,18,57)
        sunrise = datetime(2016,4,6,5,37)
        calc_sunrise, calc_sunset = rise_set(brecon, now)
        assert np.abs(sunset - calc_sunset) < timedelta(seconds=600)
        assert np.abs(sunrise - calc_sunrise) < timedelta(seconds=600)


    def test_twilight_exposure(self):
        brecon = setup()
        now = datetime(2016,4,6,19,0)
        exposure = set_exposure(brecon, now)
        assert exposure == DAY_EXP

    def test_twilight_exposur2(self):
        brecon = setup()
        now = datetime(2016,4,6,19,20)
        exposure = set_exposure(brecon, now)
        assert exposure == NIGHT_EXP/10.
