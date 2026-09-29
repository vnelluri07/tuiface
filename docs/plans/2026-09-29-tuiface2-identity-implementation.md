# tuiFace2 Identity Fix Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Give tuiFace2 a unique Pebble application identity so Pebble Core installs its World Clock-enabled PBW instead of the upstream tuiface package.

**Architecture:** Keep the World Clock implementation and stable persisted identifiers unchanged. Correct only package identity and visible configuration branding, with a source-level metadata regression test integrated into the existing `make test` entry point.

**Tech Stack:** Pebble SDK, C, PebbleKit JS/Clay JSON, Python 3 standard library, GNU Make, Unity tests.

---

### Task 1: Add package identity regression test

**Files:**
- Create: `test/test_package_metadata.py`
- Modify: `Makefile`

**Step 1: Write the failing test**

Create `test/test_package_metadata.py`:

```python
import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_UUID = uuid.UUID("a4bfc6a1-5c48-431f-b996-03b83f2ca653")
EXPECTED_UUID = uuid.UUID("35a68f22-506a-49eb-adda-56935e25c3a0")

package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
pebble = package["pebble"]

assert package["name"] == "tuiface2"
assert package["author"] == "vnelluri"
assert package["version"] == "1.2.0"
assert pebble["displayName"] == "tuiFace2"
assert uuid.UUID(pebble["uuid"]) == EXPECTED_UUID
assert uuid.UUID(pebble["uuid"]) != UPSTREAM_UUID
assert "SETTINGS_TZ_OFFSET" in pebble["messageKeys"]

print("Package metadata is valid for tuiFace2")
```

Add `metadata-test` to `.PHONY`, make `test` depend on it, and run the script with `python3 test/test_package_metadata.py`.

**Step 2: Run the test to verify it fails**

Run: `wsl python3 test/test_package_metadata.py`

Expected: FAIL because the package name is still `tuiface`.

**Step 3: Commit the failing regression test**

```powershell
git add Makefile test/test_package_metadata.py
git commit -m "test: guard tuiFace2 package identity"
```

### Task 2: Correct application identity and branding

**Files:**
- Modify: `package.json`
- Modify: `src/pkjs/config.json`

**Step 1: Apply minimal metadata changes**

Set these values in `package.json`:

```json
{
  "name": "tuiface2",
  "author": "vnelluri",
  "version": "1.2.0",
  "pebble": {
    "displayName": "tuiFace2",
    "uuid": "35a68f22-506a-49eb-adda-56935e25c3a0"
  }
}
```

Preserve all other package fields, message keys, capabilities, resources, and target platforms.

Change the Clay configuration title in `src/pkjs/config.json` from `tuiface Settings` to `tuiFace2 Settings`.

**Step 2: Run the metadata test to verify it passes**

Run: `wsl python3 test/test_package_metadata.py`

Expected: PASS with `Package metadata is valid for tuiFace2`.

**Step 3: Run the complete available host suite**

Run: `wsl make -C test test`

Expected: 33 tests, 0 failures.

Run when formatter is available: `make test`

Expected: formatting check and all tests pass.

**Step 4: Commit the implementation**

```powershell
git add package.json src/pkjs/config.json
git commit -m "fix: give tuiFace2 a unique app identity"
```

### Task 3: Build and inspect the Emery PBW

**Files:**
- Generated, not committed: `build/tuiface2.pbw` or the Pebble SDK's equivalent output

**Step 1: Build**

Activate the repository Pebble SDK environment and run:

```text
pebble build
```

Expected: Emery build succeeds and produces a PBW.

**Step 2: Inspect packaged metadata**

Open the PBW as a ZIP and verify `appinfo.json` contains:

- UUID `35a68f22-506a-49eb-adda-56935e25c3a0`
- version `1.2.0`
- display/package name `tuiFace2`/`tuiface2`
- company/author `vnelluri`
- `SETTINGS_TZ_OFFSET`

Inspect `pebble-js-app.js` and verify it contains `World Clock Timezone` and five `World Clock` slot options.

**Step 3: Keep generated artifacts untracked**

Run: `git status --short`

Expected: no generated PBW or build output is staged.

### Task 4: Review and publish the branch

**Files:**
- Review all changed files

**Step 1: Review the diff**

Run: `git diff main...HEAD`

Verify there are no changes to World Clock source identifiers, persistence keys, or unrelated behavior.

**Step 2: Run final verification**

Run the metadata test and 33-test host suite again. Run the full formatter/build checks where the required tools are available.

**Step 3: Push the branch**

```powershell
git push -u origin tuiface2-identity-fix
```

**Step 4: Open the pull request**

Create a PR titled `fix: give tuiFace2 a unique app identity`. Explain the duplicate UUID/version root cause, changed metadata, new-install impact, validation evidence, and requirement for a new Rebble listing after merge.
