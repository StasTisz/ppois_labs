import pytest
from lab2.domain.academics.subject import Subject
from lab2.domain.people.lecturer import Lecturer
from lab2.domain.people.student import Student
from lab2.domain.schedule.classroom import Classroom
from lab2.domain.schedule.lesson import Lesson
from lab2.domain.schedule.timeslot import Timeslot
from lab2.domain.structure.academic_group import AcademicGroup
from lab2.domain.structure.speciality import Speciality


def test_lesson():
    subj = Subject("ООП", 1)
    l = Lecturer("L", "L")
    g = AcademicGroup("1", Speciality("1", "1"), max_students=5)
    ts = Timeslot(1, "10:00", "11:30")
    room = Classroom("101", 30, has_computers=True)

    les = Lesson(subj, l, g, room, ts, 1)
    assert les.subject == subj

    small_room = Classroom("102", 0)
    g.enroll_student(Student("1", "1"))
    with pytest.raises(ValueError, match="мала для группы"):
        Lesson(subj, l, g, small_room, ts, 1)

    lab_subj = Subject("Лабораторная работа", 1)
    no_pc_room = Classroom("103", 20, has_computers=False)
    with pytest.raises(ValueError, match="нужна компьютерная аудитория"):
        Lesson(lab_subj, l, g, no_pc_room, ts, 1)
