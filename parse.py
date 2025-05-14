import json

from board import Board


def export(b: Board) -> str:
    out = json.dumps({"version": b.FORMAT_VERSION}) + "\n"
    for i in range(9):
        for j in range(9):
            v = b[i, j]
            if v is None:
                out += "_"
            else:
                out += str(v)
            if j < 8:
                out += " "
        out += "\n"

    return out


def parse_str(cnt: str) -> Board:
    board = Board()
    lines = cnt.strip().split("\n")
    info = json.loads(lines[0])
    if info["version"] == 1.0:
        for i, l in enumerate(lines[1:]):
            crs = l.split(" ")
            assert len(crs) == 9, crs
            for j, c in enumerate(crs):
                cc = c.strip()
                if cc == "_":
                    continue
                board[i, j] = int(cc)
        return board
    assert False, f"Format v{info["version"]} not yet supported"


def parse_file(path: str) -> Board:
    with open(path, "r", encoding="utf-8") as f:
        cnt = f.read()
    return parse_str(cnt)


def main():
    a = parse_file("tests/test3.txt")
    b = parse_file("tests/test1.txt")
    # c = read_txt("tests/base.txt")
    print(a)
    print(b)
    print(export(b))
    print(parse_str(export(b)))


if __name__ == "__main__":
    main()
