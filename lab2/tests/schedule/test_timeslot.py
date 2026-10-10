from lab2.domain.schedule.timeslot import Timeslot


def test_timeslot():
    ts = Timeslot(1, "08:15", "09:45")
    assert ts.sequence_number == 1
    assert ts.duration_minutes == 90
