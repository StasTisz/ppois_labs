from lab2.domain.schedule.timeslot import Timeslot


def test_timeslot():
    ts1 = Timeslot(1, "08:15", "09:45")
    assert ts1.sequence_number == 1
    assert ts1.duration_minutes == 90
    assert "Пара #1" in ts1.format_timeslot()
    assert "Timeslot" in repr(ts1)

    ts2 = Timeslot(2, "10:00", "11:30")
    assert ts1.conflicts_with(ts2) is False

    ts1_duplicate = Timeslot(1, "08:15", "09:45")
    assert ts1.conflicts_with(ts1_duplicate) is True
    assert ts1 == ts1_duplicate
    assert ts1 != ts2
    assert ts1 != "NotATimeslot"
    assert len({ts1, ts1_duplicate}) == 1
