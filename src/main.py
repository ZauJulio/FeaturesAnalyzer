#!/usr/bin/env python3  # noqa: EXE001
import sys

from dotenv import load_dotenv

from app import FeaturesAnalyzer

load_dotenv()


def main() -> int:
    """The application's entry point."""
    app = FeaturesAnalyzer()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
