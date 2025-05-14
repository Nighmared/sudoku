import parse
from main import generate_and_del, solve


def main():
    print("[1/5] Checking parsing")
    _ = parse.parse_file("tests/base.txt")  # check format
    a = parse.parse_file("tests/test1.txt")
    b = parse.parse_file("tests/test3.txt")
    c = parse.parse_file("tests/test9_hard.txt")
    print("✔")
    print("[2/5] Equality sanity Check")
    assert a != b
    print("✔")
    print("[3/5] Checking Exporter")
    aa = parse.parse_str(parse.export(a))
    assert aa == a
    print("✔")
    print("[4/5] Checking Solver")
    print("\t1.")
    # print(a)
    solve(a)  # solve already checks for completeness and validity
    # print(a)
    print("\t2.")
    # print(b)
    solve(b)
    # print(b)
    print("\t3. Hard one")
    # print(c)
    solve(c)
    # print(c)
    print("✔")
    print("[5/5] Testing generator")
    # for generation of sudokus to be played
    # has to still have Nones in there, but be valid
    x = generate_and_del()
    assert x.check_valid()
    assert not x.check_valid(no_none=True)
    print("✔")


if __name__ == "__main__":
    main()
