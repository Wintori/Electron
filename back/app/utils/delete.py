def delete_from_dict(d: dict, value) -> None:
    stack = [value]

    while stack:
        cur = stack.pop()
        try:
            stack += d.pop(cur)
        except KeyError:
            pass
        print(stack)

    delete_from_value(d, value)


def delete_from_value(d, value):
    for i in d.values():
        try:
            i.remove(value)
        except ValueError:
            pass


def get_tree_keys(tree: dict) -> list:
    res = []

    for val in tree.values():
        res += val

    return res
