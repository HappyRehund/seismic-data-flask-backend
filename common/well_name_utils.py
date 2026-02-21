import re


def normalize_well_name(name: str) -> str:

    name = name.strip().upper()

    bare = name.removeprefix("GNK-")

    match = re.fullmatch(r"(\d+)([A-Z]*)", bare)
    if not match:
        return name

    number, suffix = match.group(1), match.group(2)
    return f"GNK-{number.zfill(3)}{suffix}"
