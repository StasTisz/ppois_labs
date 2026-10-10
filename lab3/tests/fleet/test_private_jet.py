from lab3.domain.fleet.private_jet import PrivateJet


def test_private_jet():
    jet = PrivateJet("Gulfstream-G650", 920.0, "N-777VIP", 15000.0, "VIP Client")
    assert jet.owner_name == "VIP Client"
    assert jet.is_vip_catered is False

    jet.order_vip_catering()
    assert jet.is_vip_catered is True

    jet.perform_maintenance()
    assert jet.satellite_comms_calibrated is True
    assert jet.requires_maintenance is False
