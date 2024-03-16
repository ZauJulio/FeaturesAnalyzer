import os


def at(path: str):
    """Return the absolute path of a file in the project.

    Args:
        path (str): The path to the file.
        Must start with: ["@layout", "@icon"]

    Returns:
        str: The absolute path of the file.
    """
    seg = path.split("/")

    return {
        "@layout": os.path.join(os.getcwd(), "ui", "layouts", f"{seg[1]}.ui"),
        "@icon": os.path.join(os.getcwd(), "..", "assets", "icons", seg[1]),
    }[seg[0]]
