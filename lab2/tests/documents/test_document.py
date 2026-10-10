import pytest
from lab2.domain.documents.document import Document
from lab2.domain.exceptions import DocumentNotSignedException
from lab2.domain.people.dean import Dean


def test_document():
    doc = Document("Документ")
    assert doc.status == "Проект"
    assert doc.is_signed is False

    with pytest.raises(DocumentNotSignedException):
        doc.cancel_document("Причина")

    dean = Dean("Декан", "Деканов")
    doc.sign(dean)
    assert doc.status == "Подписан"
    assert doc.is_signed is True
    assert doc.signer == dean

    with pytest.raises(ValueError):
        doc.sign(dean)

    doc.cancel_document("Ошибочный")
    assert doc.status == "Проект"
    assert "АННУЛИРОВАН: Ошибочный" in doc.title
