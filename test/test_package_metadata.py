import json
import re
from pathlib import Path
from uuid import UUID


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = REPOSITORY_ROOT / "package.json"
CONFIG_PATH = REPOSITORY_ROOT / "src" / "pkjs" / "config.json"
UPSTREAM_UUID = "a4bfc6a1-5c48-431f-b996-03b83f2ca653"
EXPECTED_UUID = "35a68f22-506a-49eb-adda-56935e25c3a0"
UPSTREAM_VERSION = (1, 1, 0)
VERSION_PATTERN = re.compile(r"\d+\.\d+\.\d+")


def require_equal(actual, expected, description):
    if actual != expected:
        raise AssertionError(
            f"{description} must be {expected!r}, got {actual!r}"
        )


with PACKAGE_PATH.open(encoding="utf-8") as package_file:
    package = json.load(package_file)

with CONFIG_PATH.open(encoding="utf-8") as config_file:
    config = json.load(config_file)

configuration_heading = next(
    (item for item in config if item.get("type") == "heading"), None
)
if configuration_heading is None:
    raise AssertionError("Clay configuration must contain a top-level heading")
require_equal(
    configuration_heading.get("defaultValue"),
    "tuiFace2 Settings",
    "configuration heading",
)

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

actual_version = package["version"]
if not isinstance(actual_version, str) or VERSION_PATTERN.fullmatch(actual_version) is None:
    raise AssertionError(
        "package version must contain three dot-separated integers, "
        f"got {actual_version!r}"
    )
parsed_version = tuple(int(component) for component in actual_version.split("."))
if parsed_version <= UPSTREAM_VERSION:
    upstream_version_text = ".".join(str(component) for component in UPSTREAM_VERSION)
    raise AssertionError(
        f"package version must be greater than upstream {upstream_version_text!r}, "
        f"got {actual_version!r}"
    )

require_equal(pebble["displayName"], "tuiFace2", "Pebble displayName")

message_keys = pebble["messageKeys"]
if "SETTINGS_TZ_OFFSET" not in message_keys:
    raise AssertionError(
        "pebble.messageKeys must contain 'SETTINGS_TZ_OFFSET', "
        f"got {message_keys!r}"
    )

print("Package metadata checks passed.")
