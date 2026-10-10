from lab3.domain.security.scanner import Scanner


class DummyScanner(Scanner):
    def scan(self, target) -> bool:
        return self.is_active


def test_scanner():
    s = DummyScanner("Scan-100")
    assert s.model == "Scan-100"
    assert s.scan(None) is True
