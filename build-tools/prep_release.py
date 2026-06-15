"""
Prepare release artifacts for the clams-vocabulary package.

Run while preparing a release PR, passing the version being released::

    python build-tools/prep_release.py X.Y.Z

This is the clams-vocabulary counterpart of the SDK-wide
``prep_release.py`` entry point. clams-vocabulary does not maintain a
``documentation/target-versions.csv``, so there is currently no
automated release-prep step here; the script exists for interface
parity with the other SDK repos and as the home for any future
clams-vocabulary release-prep automation.
"""
import argparse
import re
import sys

VERSION_RE = re.compile(r'^\d+\.\d+\.\d+$')


def main():
    parser = argparse.ArgumentParser(
        description="Prepare release artifacts for clams-vocabulary."
    )
    parser.add_argument(
        "version", metavar="X.Y.Z",
        help="the release version being prepared",
    )
    args = parser.parse_args()

    if not VERSION_RE.match(args.version):
        sys.exit(f"Error: '{args.version}' is not a valid X.Y.Z version.")

    print("No automated release-prep steps for clams-vocabulary "
          f"({args.version}); nothing to do.")


if __name__ == "__main__":
    main()
