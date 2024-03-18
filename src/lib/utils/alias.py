import os


def at(path: str):
    """Return the absolute path of a file in the project.

    Args:
        path (str): The path to the file.
        Must start with: ["@layout", "@icon"]
        and followed by the path to the file using "/" as separator.

    Returns:
        str: The absolute path of the file.
    """
    seg = path.split("/")

    if len(seg) < 2:
        raise ValueError("Invalid path.")

    tag = seg[0]
    paths = os.sep.join(seg[1:])

    return {
        "@icon": os.path.join(os.getcwd(), "..", "assets", "icons", paths),
        "@layout": os.path.join(os.getcwd(), "ui", "layouts", f"{paths}.ui"),
    }[tag]
