import pytest
from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.baggage_tractor import BaggageTractor


def test_baggage_tractor():
    tractor = BaggageTractor("Clark-CT", 30.0, "BT-01", max_carts=3)
    assert tractor.current_carts == 0

    tractor.attach_cart()
    tractor.attach_cart()
    assert tractor.current_carts == 2

    tractor.attach_cart()
    with pytest.raises(CapacityExceededException):
        tractor.attach_cart()

    tractor.detach_all_carts()
    assert tractor.current_carts == 0

    tractor.perform_maintenance()
    assert tractor.tow_hitch_greased is True
