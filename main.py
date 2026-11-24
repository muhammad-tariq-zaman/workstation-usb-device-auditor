"""Audit USB devices plugged into workstations.

Usage: python3 main.py usb.csv
CSV columns: workstation,device,device_class,approved.
device_class is storage, input or other; approved is yes or
no. Verdicts:
- UNAPPROVED STORAGE: a storage device (USB stick, external
  drive) that is not approved — data can walk out the door.
- UNAPPROVED: any other device class that is not approved.
- APPROVED: an approved device.
UNAPPROVED STORAGE first, then UNAPPROVED, then APPROVED;
within a verdict by workstation, then device. Rows with an
unknown device_class or an approved value other than yes/no
are reported as skipped, not silently dropped.
"""
import argparse, csv, sys

VERDICT_ORDER = {"UNAPPROVED STORAGE": 0, "UNAPPROVED": 1, "APPROVED": 2}
CLASSES = {"storage", "input", "other"}

def audit(rows):
    out = []
    skipped = 0
    for row in rows:
        try:
            workstation = row["workstation"].strip()
            device = row["device"].strip()
            device_class = row["device_class"].strip().lower()
            approved = row["approved"].strip().lower()
            if not workstation or not device or device_class not in CLASSES \
                    or approved not in ("yes", "no"):
                raise ValueError("bad value")
        except (KeyError, AttributeError, ValueError, TypeError):
            skipped += 1
            continue
        if approved == "yes":
            verdict, detail = "APPROVED", f"{device_class} device, approved"
        elif device_class == "storage":
            verdict = "UNAPPROVED STORAGE"
            detail = "storage device, not approved"
        else:
            verdict = "UNAPPROVED"
            detail = f"{device_class} device, not approved"
        out.append((workstation, device, verdict, detail))
    out.sort(key=lambda r: (VERDICT_ORDER[r[2]], r[0], r[1]))
    return out, skipped

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results, skipped = audit(list(csv.DictReader(f)))
    for workstation, device, verdict, detail in results:
        print(f"{workstation} {device}: {verdict} - {detail}")
    counts = {v: sum(1 for *_, verdict, _ in results if verdict == v)
              for v in VERDICT_ORDER}
    print(f"{counts['UNAPPROVED STORAGE']} unapproved storage device(s), "
          f"{counts['UNAPPROVED']} other unapproved device(s), "
          f"{counts['APPROVED']} approved out of {len(results)} device(s).")
    if skipped:
        print(f"Skipped {skipped} invalid row(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
