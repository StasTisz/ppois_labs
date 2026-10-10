import pytest
from lab2.domain.academics.subject import Subject
from lab2.domain.exceptions import ScheduleCollisionException
from lab2.domain.people.lecturer import Lecturer
from lab2.domain.schedule.classroom import Classroom
from lab2.domain.schedule.lesson import Lesson
from lab2.domain.schedule.timeslot import Timeslot
from lab2.domain.schedule.timetable import Timetable
from lab2.domain.structure.academic_group import AcademicGroup
from lab2.domain.structure.speciality import Speciality


def test_timetable():
    tt = Timetable(1)
    room = Classroom("101", 30)
    ts = Timeslot(1, "10:00", "11:30")
    subj = Subject("S", 1)
    l = Lecturer("L", "L")
    g = AcademicGroup("1", Speciality("1", "1"))

    lesson = Lesson(subj, l, g, room, ts, 1)
    tt.add_lesson(lesson)

    room.close_for_maintenance()
    lesson2 = Lesson(subj, l, g, room, ts, 2)
    with pytest.raises(ScheduleCollisionException, match="закрыта на ремонт"):
        tt.add_lesson(lesson2)
    room.open_classroom()

    l_other = Lecturer("L2", "L2")
    g_other = AcademicGroup("2", Speciality("1", "1"))
    coll_room = Lesson(subj, l_other, g_other, room, ts, 1)
    with pytest.raises(ScheduleCollisionException, match="аудитория 101 уже занята"):
        tt.add_lesson(coll_room)

    other_room = Classroom("102", 30)
    coll_group = Lesson(subj, l_other, g, other_room, ts, 1)
    with pytest.raises(ScheduleCollisionException, match="уже есть пара"):
        tt.add_lesson(coll_group)

    coll_lect = Lesson(subj, l, g_other, other_room, ts, 1)
    with pytest.raises(ScheduleCollisionException, match="уже ведет пару"):
        tt.add_lesson(coll_lect)

    assert len(tt.get_schedule_for_group(g, 1)) == 1
    assert len(tt.get_schedule_for_group("1", 1)) == 1
    assert len(tt.get_lecturer_schedule(l, 1)) == 1
    assert len(tt.get_lecturer_schedule(l.person_id, 1)) == 1
