from lab3.domain.people.check_in_agent import CheckInAgent


def test_check_in_agent():
    agent = CheckInAgent("Ольга", "О", "P-444", 950.0, typing_speed=210)
    assert agent.passengers_processed == 0
    msg = agent.perform_duty()
    assert agent.passengers_processed == 1
    assert "итого: 1" in msg
