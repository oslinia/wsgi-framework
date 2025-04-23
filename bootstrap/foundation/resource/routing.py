from ..http.routing.map import Mapper


def build_mask(items: list[tuple[int, tuple[str, ...]] | None]):
    if items is not None:
        mask = ''.join((f"        {num}: {masks},\n" for num, masks in items))

        return f"{{\n{mask}    }}"

    return None


def build_link(items: list[tuple[int, str, str]]):
    return ''.join((f"        {num}: ('{path}', r'{pattern}'),\n" for num, path, pattern in items))


def routing(mapper: Mapper):
    patterns, masks, links = (s if '' == s else f"\n{s}" for s in (
        ''.join((f"    (r'{pattern}', '{name}'),\n" for pattern, name in mapper.patterns)),
        ''.join((f"    '{name}': {build_mask(items)},\n" for name, items in mapper.masks.items())),
        ''.join((f"    '{name}': {{\n{build_link(items)}    }},\n" for name, items in mapper.links.items())),
    ))

    return (f"patterns = ({patterns})\n\n"
            f"masks = {{{masks}}}\n\n"
            f"links = {{{links}}}\n")


def write(file: str):
    with open(file, 'w') as f:
        f.write(routing(Mapper()))
