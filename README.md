# workstation-usb-device-auditor

Audit USB devices plugged into workstations: the input CSV lists workstation, device, device_class (storage, input or other) and approved (yes/no) — UNAPPROVED STORAGE for a storage device (USB stick, external drive) that is not approved, since data can walk out the door, UNAPPROVED for any other device class that is not approved, APPROVED for an approved device — UNAPPROVED STORAGE first, then UNAPPROVED, then APPROVED. Rows with an unknown device_class or an approved value other than yes/no are reported as skipped, not silently dropped.

Sample input is included (sample.csv with seven devices, one invalid row).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
WS-01 Kingston 64GB: UNAPPROVED STORAGE - storage device, not approved
WS-03 SanDisk 128GB: UNAPPROVED STORAGE - storage device, not approved
WS-02 Unknown Dongle: UNAPPROVED - input device, not approved
WS-01 HP Keyboard: APPROVED - input device, approved
WS-01 Logitech Mouse: APPROVED - input device, approved
WS-02 Seagate Backup: APPROVED - storage device, approved
2 unapproved storage device(s), 1 other unapproved device(s), 3 approved out of 6 device(s).
Skipped 1 invalid row(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
