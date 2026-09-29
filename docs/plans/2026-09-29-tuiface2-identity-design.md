# tuiFace2 Identity Fix Design

**Date:** 2026-09-29

## Purpose

Give the World Clock fork a unique Pebble application identity so Pebble Core no longer confuses it with the upstream `tuiface` watchface.

## Problem

The upstream watchface and the fork currently share all identity fields that Pebble uses to distinguish installed applications:

- UUID `a4bfc6a1-5c48-431f-b996-03b83f2ca653`
- version `1.1.0`
- package and display name `tuiface`
- author `Elizardbeth`

The upstream PBW does not contain World Clock, while the fork PBW does. Because the UUID and version are identical, Pebble Core can retain or select the upstream package and display its configuration without World Clock.

## Approved approach

Assign the fork a newly generated UUID and fork-specific metadata:

- package name: `tuiface2`
- display name: `tuiFace2`
- author: `vnelluri`
- version: `1.2.0`
- configuration title: `tuiFace2 Settings`

The World Clock implementation, complication identifier `19`, persistence key `1018`, and existing message keys will remain unchanged.

## Regression protection

Add an automated metadata test that reads `package.json` and verifies:

- the UUID is valid and differs from the upstream UUID;
- package and display names identify tuiFace2;
- the author is `vnelluri`;
- the version is greater than `1.1.0`;
- the World Clock message key remains present.

Integrate this check into the repository's standard `make test` entry point.

## Validation

1. Run the metadata test before implementation and confirm it fails for the identity collision.
2. Update metadata and configuration branding, then confirm the metadata test passes.
3. Run all 33 existing host tests, including the six World Clock tests.
4. Run the formatting check when `clang-format` is available.
5. Build the Emery PBW when the Pebble SDK is available.
6. Inspect the PBW's `appinfo.json` and bundled JavaScript to verify the new identity and World Clock settings.

## Release impact

The corrected package is a new Pebble application. Existing settings stored under the colliding UUID will not transfer. The current Rebble listing cannot safely represent the new identity, so the corrected PBW requires a new listing. The existing listing should remain available until the replacement is installed and verified, then be hidden or clearly deprecated.
