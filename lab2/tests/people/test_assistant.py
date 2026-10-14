import pytest

from lab2.domain.academics.labwork import LabWork
from lab2.domain.academics.subject import Subject
from lab2.domain.people.assistant import Assistant
from lab2.domain.people.student import Student
from lab2.domain.schedule.classroom import Classroom
from lab2.domain.structure.academic_group import AcademicGroup
from lab2.domain.structure.speciality import Speciality


def test_assistant():
    ass = Assistant("Ассистент", "Ассистентов")
    assert ass.degree == "Магистр"
    assert ass.position == "Преподаватель"

    subj = Subject("Информатика", 1)
    lab = LabWork("Основы", 10.0, lab_number=1)
    group = AcademicGroup("101", Speciality("ПОИТ", "POIT-01"))
    student = Student("Иван", "Иванов")

    msg = ass.conduct_lab(subj, lab, group)
    assert "провел лабораторную" in msg

    assert ass.grade_labwork(student, lab, 9.5) == 9.5
    with pytest.raises(ValueError):
        ass.grade_labwork(student, lab, 15.0)

    room = Classroom("204-1", 30, has_projector=True, has_computers=True)
    assert ass.prepare_lab_equipment(room) is True

    room.close_for_maintenance()
    with pytest.raises(ValueError):
        ass.prepare_lab_equipment(room)
