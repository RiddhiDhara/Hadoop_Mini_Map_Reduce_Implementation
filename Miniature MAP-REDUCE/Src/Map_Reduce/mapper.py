def apply_where(row, where_clause):
    """
    Evaluates WHERE condition dynamically
    """

    if not where_clause:
        return True

    left = where_clause["left"]
    op = where_clause["op"]
    right = where_clause["right"]

    if op == ">":
        return row[left] > right
    elif op == "<":
        return row[left] < right
    elif op == "==":
        return row[left] == right
    elif op == ">=":
        return row[left] >= right
    elif op == "<=":
        return row[left] <= right
    else:
        raise ValueError(f"Unsupported operator: {op}")


def map_partition(partition, query):
    """
    SQL-correct mapper:
    emits (group_key, (agg_type, value))
    """

    intermediate = []

    where_clause = query["where"]
    group_by_key = query["group_by"][0]
    aggregations = query["select"]["aggregations"]

    for row in partition:

        # WHERE filter
        if not apply_where(row, where_clause):
            continue

        key = row[group_by_key]

        for agg in aggregations:

            func = agg["func"]
            col = agg["column"]

            # COUNT(*)
            if func == "COUNT" and col == "*":
                intermediate.append((key, ("COUNT", 1)))

            # SUM / AVG use real column values
            else:
                value = row[col]

                if func == "SUM":
                    intermediate.append((key, ("SUM", value)))

                elif func == "AVG":
                    intermediate.append((key, ("AVG", value)))

    return intermediate


