import json
from pathlib import Path
from uuid import UUID


PACKAGE_PATH = Path(__file__).resolve().parents[1] / "package.json"
UPSTREAM_UUID = "a4bfc6a1-5c48-431f-b996-03b83f2ca653"
EXPECTED_UUID = "35a68f22-506a-49eb-adda-56935e25c3a0"


def require_equal(actual, expected, description):
    if actual != expected:
        raise AssertionError(
            f"{description} must be {expected!r}, got {actual!r}"
        )


with PACKAGE_PATH.open(encoding="utf-8") as package_file:
    package = json.load(package_file)

pebble = package["pebble"]

actual_uuid_text = pebble["uuid"]
try:
    actual_uuid = UUID(actual_uuid_text)
except (AttributeError, TypeError, ValueError) as error:
    raise AssertionError(
        f"Pebble UUID must be a valid UUID, got {actual_uuid_text!r}"
    ) from error

if actual_uuid == UUID(UPSTREAM_UUID):
    raise AssertionError(
        f"Pebble UUID must differ from upstream UUID {UPSTREAM_UUID!r}, "
        f"got {actual_uuid_text!r}"
    )
if actual_uuid != UUID(EXPECTED_UUID):
    raise AssertionError(
        f"Pebble UUID must be {EXPECTED_UUID!r}, got {actual_uuid_text!r}"
    )

require_equal(package["name"], "tuiface2", "package name")
require_equal(package["author"], "vnelluri", "package author")
require_equal(package["version"], "1.2.0", "package version")
require_equal(pebble["displayName"], "tuiFace2", "Pebble displayName")

message_keys = pebble["messageKeys"]
if "SETTINGS_TZ_OFFSET" not in message_keys:
    raise AssertionError(
        "pebble.messageKeys must contain 'SETTINGS_TZ_OFFSET', "
        f"got {message_keys!r}"
    )

print("Package metadata checks passed.")
