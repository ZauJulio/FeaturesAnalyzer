#!/usr/bin/env python3  # noqa: EXE001
import sys

from app import FeaturesAnalyzer


def main() -> int:
    """The application's entry point."""
    app = FeaturesAnalyzer()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
