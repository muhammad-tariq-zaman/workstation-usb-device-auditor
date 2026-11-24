import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import audit

def row(workstation, device, device_class, approved):
    return {"workstation": workstation, "device": device,
            "device_class": device_class, "approved": approved}

class TestUsbAuditor(unittest.TestCase):
    def test_unapproved_storage(self):
        r, _ = audit([row("WS-01", "Kingston 64GB", "storage", "no")])
        self.assertEqual(r[0][2], "UNAPPROVED STORAGE")

    def test_approved_storage_is_ok(self):
        r, _ = audit([row("WS-01", "Seagate Backup", "storage", "yes")])
        self.assertEqual(r[0][2], "APPROVED")

    def test_unapproved_input(self):
        r, _ = audit([row("WS-02", "Unknown Dongle", "input", "no")])
        self.assertEqual(r[0][2], "UNAPPROVED")

    def test_approved_input(self):
        r, _ = audit([row("WS-01", "Logitech Mouse", "input", "yes")])
        self.assertEqual(r[0][2], "APPROVED")

    def test_storage_comes_first(self):
        r, _ = audit([row("WS-01", "Logitech Mouse", "input", "no"),
                      row("WS-02", "Kingston 64GB", "storage", "no")])
        self.assertEqual(r[0][1], "Kingston 64GB")

    def test_unknown_class_is_skipped(self):
        r, skipped = audit([row("WS-01", "Weird Thing", "magic", "no"),
                            row("WS-01", "Logitech Mouse", "input", "yes")])
        self.assertEqual((len(r), skipped), (1, 1))

    def test_bad_approved_value_is_skipped(self):
        r, skipped = audit([row("WS-01", "Mouse", "input", "maybe")])
        self.assertEqual((r, skipped), ([], 1))

    def test_empty_input(self):
        self.assertEqual(audit([]), ([], 0))
