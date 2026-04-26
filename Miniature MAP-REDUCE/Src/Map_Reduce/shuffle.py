from collections import defaultdict


def shuffle(mapped_partitions, num_reducers=4):
    """
    Groups mapper output by:
    1. key (GROUP BY column)
    2. aggregation type (COUNT / SUM / AVG)
    and assigns to reducers
    """

    # reducer_id → key → agg_type → list(values)
    reducer_buckets = [
        defaultdict(lambda: defaultdict(list))
        for _ in range(num_reducers)
    ]

    for partition in mapped_partitions:

        for key, (agg_type, value) in partition:

            # assign reducer using hash partitioning
            reducer_id = hash(key) % num_reducers

            # group by key + aggregation type
            reducer_buckets[reducer_id][key][agg_type].append(value)

    return reducer_buckets




