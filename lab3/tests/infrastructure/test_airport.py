from lab3.domain.infrastructure.airport import Airport
from lab3.domain.infrastructure.terminal import Terminal


def test_airport():
    ap = Airport("Minsk-2", "MSQ")
    term = Terminal("T1")
    ap.add_terminal(term)

    assert ap.name == "Minsk-2"
    assert ap.iata_code == "MSQ"
    assert ap.get_terminal("T1") == term
    assert ap.get_terminal("Unknown") is None
