from lab2.domain.people.dean import Dean


def test_dean():
    dean = Dean("Декан", "Деканов")
    result = dean.sign_order("Отчислить студента")
    assert "ПРИКАЗ УТВЕРЖДЕН: Отчислить студента" in result
    assert "Деканов Декан" in result
