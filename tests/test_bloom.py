from src.structures.bloom import BloomFilter


def test_no_false_negatives():
    bf = BloomFilter(n=100, fp_rate=0.01)

    items = list(range(100))
    bf.build(items)

    for x in items:
        assert bf.query(x) is True


def test_reasonable_fp_rate():
    bf = BloomFilter(n=100, fp_rate=0.1)

    inserted = list(range(100))
    bf.build(inserted)

    test_items = list(range(100, 200))

    positives = sum(1 for x in test_items if bf.query(x))

    # allow loose bound
    assert positives < 30
