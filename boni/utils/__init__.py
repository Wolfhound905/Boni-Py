from os import walk


def get_cogs(path: str) -> list:
    """Get scales"""
    files = [thing for thing in walk(path)][0][2]
    scales = [x.replace(".py", "").replace(" ", "_") for x in files]
    return ["boni.cogs.{}".format(x) for x in scales]
