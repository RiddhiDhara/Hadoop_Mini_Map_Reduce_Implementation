def reduce_partition(grouped_data, query):
    """
    SQL-correct reducer:
    grouped_data format:
        key -> { agg_type -> [values] }
    """

    aggregations = query["select"]["aggregations"]
    result = {}

    for key, agg_dict in grouped_data.items():

        result[key] = {}

        for agg in aggregations:

            func = agg["func"]

            # get values for this aggregation type
            values = agg_dict.get(func, [])

            # ---------------- COUNT ----------------
            if func == "COUNT":
                result[key]["COUNT"] = sum(values)  # safer than len()

            # ---------------- SUM ----------------
            elif func == "SUM":
                result[key]["SUM"] = sum(values)

            # ---------------- AVG ----------------
            elif func == "AVG":
                result[key]["AVG"] = (
                    sum(values) / len(values) if values else 0
                )

    return result