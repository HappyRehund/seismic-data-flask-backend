import re


def normalize_well_name(name: str) -> str:

    name = name.strip().upper()

    bare = name.removeprefix("MJ-")

    match = re.fullmatch(r"(\d+)([A-Z]*)", bare)
    if not match:
        return name

    number, suffix = match.group(1), match.group(2)
    return f"MJ-{number.zfill(3)}{suffix}"
