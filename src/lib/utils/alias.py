import os


def at(path: str) -> str:
    """
    Return the absolute path of a file in the project.

    Args:
    ----
        path (str): The path to the file.
        Must start with: ["@layout", "@icon"]
        and followed by the path to the file using "/" as separator.

    Returns:
    -------
        str: The absolute path of the file.

    """
    seg = path.split("/")
    min_depth = 2

    if len(seg) < min_depth:
        msg = "Invalid path."
        raise ValueError(msg)

    tag = seg[0]
    cwd = os.getcwd()  # noqa: PTH109
    paths = os.sep.join(seg[1:])  # noqa: PTH118

    return {
        "@icon": os.path.join(cwd, "..", "assets", "icons", paths),  # noqa: PTH118
        "@layout": os.path.join(cwd, "ui", "layouts", f"{paths}.ui"),  # noqa: PTH118
    }[tag]
