import sys
import time
from random import choice, randint

from board import Board
from parse import parse_file

NUM_DEL = 45
VERBOSE = True


def fill_rec(b: Board, next_idx: int) -> bool:
    if next_idx == 81:
        return b.check_valid()
    r, c = Board.i_to_rc(next_idx)
    if b[r, c] is not None:  # we are solving instead of generating lol
        return fill_rec(b, next_idx + 1)

    options: set[int] = b.get_options(r, c)
    if len(options) == 0:
        return False
    while len(options) > 0:
        test = choice(list(options))
        options.remove(test)
        b[r, c] = test
        if fill_rec(b, next_idx + 1):
            return True

    b[r, c] = None
    return False  # hope this is correct here


def solve(b: Board):
    start = time.time()
    fill_rec(b, 0)
    end = time.time()
    if VERBOSE:
        print(f"solved in {(end-start):.2f}s")
    assert b.check_valid(no_none=True)


def generate_complete() -> Board:
    b = Board()
    fill_rec(b, 0)
    assert b.check_valid(no_none=True)
    return b


def generate_and_del(target_del: int = NUM_DEL):
    b = generate_complete()
    del_count = 0
    while del_count < target_del:
        dr = randint(0, 8)
        dc = randint(0, 8)
        if b[dr, dc] is not None:
            del_count += 1
            b[dr, dc] = None
    return b


def main():
    c = NUM_DEL
    if len(sys.argv) > 1:
        c = int(sys.argv[1])
    print(generate_and_del(c))


if __name__ == "__main__":
    main()
