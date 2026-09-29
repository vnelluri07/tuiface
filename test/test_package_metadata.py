import json
from pathlib import Path


PACKAGE_PATH = Path(__file__).resolve().parents[1] / "package.json"
UPSTREAM_UUID = "a4bfc6a1-5c48-431f-b996-03b83f2ca653"
EXPECTED_UUID = "35a68f22-506a-49eb-adda-56935e25c3a0"

with PACKAGE_PATH.open(encoding="utf-8") as package_file:
    package = json.load(package_file)

pebble = package["pebble"]

assert package["name"] == "tuiface2", (
    f"package name must be 'tuiface2', got {package['name']!r}"
)
assert package["author"] == "vnelluri", (
    f"package author must be 'vnelluri', got {package['author']!r}"
)
assert package["version"] == "1.2.0", (
    f"package version must be '1.2.0', got {package['version']!r}"
)
assert pebble["displayName"] == "tuiFace2", (
    f"Pebble displayName must be 'tuiFace2', got {pebble['displayName']!r}"
)
assert pebble["uuid"] == EXPECTED_UUID, (
    f"Pebble UUID must be {EXPECTED_UUID!r}, got {pebble['uuid']!r}"
)
assert pebble["uuid"] != UPSTREAM_UUID, (
    f"Pebble UUID must differ from upstream UUID {UPSTREAM_UUID!r}"
)
assert "SETTINGS_TZ_OFFSET" in pebble["messageKeys"], (
    "SETTINGS_TZ_OFFSET must remain in pebble.messageKeys"
)

print("Package metadata checks passed.")
