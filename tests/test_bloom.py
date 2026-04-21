from src.structures.bloom import BloomFilter


def test_no_false_negatives():
    bf = BloomFilter(n=100, fp_rate=0.1)
    items = list(range(100))
    bf.build(items)

    for x in items:
        assert bf.query(x)


def test_reasonable_false_positives():
    bf = BloomFilter(n=100, fp_rate=0.1)
    bf.build(range(100))

    positives = sum(bf.query(x) for x in range(100, 200))

    # should not be wildly off
    assert positives < 20


def test_fp_rate_sanity():
    bf = BloomFilter(n=1000, fp_rate=0.01)
    bf.build(range(1000))

    trials = 2000
    false_pos = sum(bf.query(x) for x in range(1000, 1000 + trials))

    observed = false_pos / trials

    # very loose bound, just sanity
    assert observed < 0.05
