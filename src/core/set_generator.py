import random


def generate_block(n, seed=None):
    if seed is not None:
        random.seed(seed)

    return set(random.sample(range(10**9), n))


def generate_mempool(block, m, overlap, seed=None):
    if seed is not None:
        random.seed(seed)

    n = len(block)

    if m < n:
        raise ValueError("mempool must be >= block size")

    if overlap < 0 or overlap > 1:
        raise ValueError("overlap must be between 0 and 1")

    k = int(overlap * n)

    block_list = list(block)
    shared = set(random.sample(block_list, k))

    remaining = m - k

    extra = set()
    while len(extra) < remaining:
        x = random.randint(0, 10**9)
        if x not in block:
            extra.add(x)

    return shared.union(extra)


def generate_sender_receiver_sets(block_size, mempool_size, overlap, seed=None):
    block = generate_block(block_size, seed)
    mempool = generate_mempool(block, mempool_size, overlap, seed)
    return block, mempool
