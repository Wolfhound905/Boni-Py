from os import walk


def get_extensions(path: str) -> list:
    """Get Extensions"""
    files = [thing for thing in walk(path)][0][2]
    extensions = [x.replace(".py", "").replace(" ", "_") for x in files]
    return ["boni.extensions.{}".format(x) for x in extensions]
