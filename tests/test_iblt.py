from src.structures.iblt import IBLT


def test_simple_recovery():
    A = set(range(100))
    B = set(range(80))

    seeds = [1, 2, 3]

    iblt_A = IBLT(size=200, seeds=seeds)
    iblt_B = IBLT(size=200, seeds=seeds)

    for x in A:
        iblt_A.add(x)

    for x in B:
        iblt_B.add(x)

    diff = iblt_A.subtract(iblt_B)

    success, pos, neg = diff.peel()

    assert success
    assert pos == A - B
    assert neg == B - A


def test_iblt_multiple_runs():
    seeds = [1, 2, 3]

    for _ in range(5):
        A = set(range(100))
        B = set(range(80))

        iblt_A = IBLT(size=200, seeds=seeds)
        iblt_B = IBLT(size=200, seeds=seeds)

        for x in A:
            iblt_A.add(x)

        for x in B:
            iblt_B.add(x)

        diff = iblt_A.subtract(iblt_B)
        success, pos, neg = diff.peel()

        assert success
        assert pos == A - B
        assert neg == B - A
