from lab3.domain.people.baggage_handler import BaggageHandler


def test_baggage_handler():
    h_manual = BaggageHandler("Григорий", "Г", "P-555", 850.0, heavy_machinery_license=False)
    assert "вручную" in h_manual.perform_duty()
    assert h_manual.tons_loaded == 0.5

    h_mach = BaggageHandler("Игорь", "И", "P-556", 1100.0, heavy_machinery_license=True)
    assert "с помощью погрузчика" in h_mach.perform_duty()
