from typing import Optional

EMPTY_CHARACTER = "␣"


class Board:
    FORMAT_VERSION = 1.0
    state: list[Optional[int]]

    def __init__(self) -> None:
        self.state = [None] * 81

    def __eq__(self, o: "Board") -> bool:
        assert (
            self.FORMAT_VERSION == o.FORMAT_VERSION
        ), "Incomparable due to Version Mismatch!!"
        for i in range(81):
            if self.state[i] != o.state[i]:
                return False
        return True

    def __str__(self) -> str:
        def a(s):
            return EMPTY_CHARACTER if s is None else str(s)

        linesep = "-" * 24 + "\n"
        x = linesep
        for i in range(9):
            x += "| "
            for j in range(9):
                x += a(self[i, j])
                x += " "
                if (j + 1) % 3 == 0:
                    x += "| "
            x += "\n"
            if (i + 1) % 3 == 0:
                x += linesep
        return x

    def __setitem__(self, k: tuple[int, int], v: Optional[int]):
        r, c = k
        self.state[r * 9 + c] = v

    def __getitem__(self, k: tuple[int, int]) -> Optional[int]:
        r, c = k
        return self.state[r * 9 + c]

    def _check_indices_valid(self, indices: list[int]) -> bool:
        found: set[Optional[int]] = set()

        for i in indices:
            if self.state[i] in found and not self.state[i] is None:
                return False
            found.add(self.state[i])
        return True
        # return True

    def get_square_indices(self, square_idx: int) -> list[int]:
        sq_row, sq_col = divmod(square_idx, 3)
        base_row = 27 * sq_row
        base_col = 3 * sq_col
        indices: list[int] = []
        for vr in range(3):
            for vc in range(3):
                indx = base_row + base_col + vr * 9 + vc
                indices.append(indx)
        return indices

    def get_row_indices(self, r: int) -> list[int]:
        base = 9 * r
        indices = [base + i for i in range(9)]
        return indices

    def get_col_indices(self, c: int) -> list[int]:
        indices = [c + 9 * i for i in range(9)]
        return indices

    def _check_square_valid(self, square_idx: int) -> bool:

        return self._check_indices_valid(self.get_square_indices(square_idx))

    def _check_row_valid(self, r: int) -> bool:

        return self._check_indices_valid(self.get_row_indices(r))

    def _check_col_valid(self, c: int) -> bool:
        return self._check_indices_valid(self.get_col_indices(c))

    def rc_to_i(self, r: int, c: int) -> int:
        return r * 9 + c

    def _get_square(self, indx: int) -> int:
        sq = 0
        if indx > 26:
            sq += 3
        if indx > 53:
            sq += 3
        sq += (indx % 9) // 3
        return sq

    def get_options(self, r, c) -> set[int]:
        options: set[int] = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        indices: set[int] = set()
        indices |= set(self.get_col_indices(c))
        indices |= set(self.get_row_indices(r))
        indices |= set(self.get_square_indices(self._get_square(self.rc_to_i(r, c))))
        for i in indices:
            v = self.state[i]
            options.discard(v)  # type: ignore
            if len(options) == 0:
                break
        return options

    def check_valid(self, no_none=False) -> bool:

        # squares
        for sq in range(9):
            if not self._check_square_valid(sq):
                return False
        for r in range(9):
            if not self._check_row_valid(r):
                return False

        for c in range(9):
            if not self._check_col_valid(c):
                return False

        if no_none:
            return None not in self.state
        return True


# 0 1 2   3 4 5   6 7 8
# 0   1     2
# mod

# a a a b b b c c c
# a a a b b b c c c
# a a a b b b c c c
# d d d
# d d d
# d d d
