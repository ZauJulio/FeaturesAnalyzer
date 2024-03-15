import sys

from app import FeaturesAnalyzer


def main():
    """The application's entry point."""
    app = FeaturesAnalyzer()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
