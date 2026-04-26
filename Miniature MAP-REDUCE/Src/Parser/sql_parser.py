
# # for this query : 

# # SELECT Score, COUNT(*)
# # FROM data
# # WHERE Score > 3
# # GROUP BY Score

# def parse_query():
#     return {
#         "select": {
#             "columns": ["Score"],
#             "aggregations": [
#                 {"func": "COUNT", "column": "*"}
#             ]
#         },
#         "from": "data",
#         "where": {
#             "left": "Score",
#             "op": ">",
#             "right": 0
#         },
#         "group_by": ["Score"]
#     }




# import re

# def parse_query(query):

#     # normalize
#     query = query.replace("\n", " ")
#     query = " ".join(query.split())

#     select_match = re.search(r"SELECT (.*?) FROM", query, re.IGNORECASE)
#     from_match = re.search(r"FROM (\w+)", query, re.IGNORECASE)

#     if not select_match or not from_match:
#         raise ValueError("Invalid SQL query format")

#     select_part = select_match.group(1)
#     from_part = from_match.group(1)

#     where_match = re.search(r"WHERE (.*?) GROUP BY", query, re.IGNORECASE)
#     group_match = re.search(r"GROUP BY (.*)", query, re.IGNORECASE)

#     where_part = where_match.group(1) if where_match else None
#     group_by_part = group_match.group(1).split(",") if group_match else []

#     select_items = [x.strip() for x in select_part.split(",")]

#     aggregations = []
#     columns = []

#     for item in select_items:
#         if "(" in item:
#             func = item.split("(")[0]
#             col = item.split("(")[1].replace(")", "")
#             aggregations.append({"func": func, "column": col})
#         else:
#             columns.append(item)

#     return {
#         "select": {
#             "columns": columns,
#             "aggregations": aggregations
#         },
#         "from": from_part,
#         "where": where_part,
#         "group_by": group_by_part
#     }








import re


def parse_where(where_str):
    """
    Converts: Score > 3
    Into: {left, op, right}
    """

    if not where_str:
        return None

    parts = where_str.strip().split()

    if len(parts) != 3:
        raise ValueError(f"Invalid WHERE clause: {where_str}")

    left, op, right = parts

    # try converting number
    try:
        right = int(right)
    except:
        pass

    return {
        "left": left,
        "op": op,
        "right": right
    }


def parse_aggregations(select_part):
    """
    Converts: COUNT(*), SUM(Score)
    """

    items = [x.strip() for x in select_part.split(",")]

    aggregations = []
    columns = []

    for item in items:

        # aggregation function
        if "(" in item and ")" in item:
            func = item.split("(")[0].strip()
            col = item.split("(")[1].replace(")", "").strip()

            aggregations.append({
                "func": func.upper(),
                "column": col
            })

        else:
            columns.append(item)

    return columns, aggregations


def parse_query(query):
    """
    Main SQL parser → returns structured IR
    """

    # normalize query
    query = query.replace("\n", " ")
    query = " ".join(query.split())

    # SELECT
    select_match = re.search(r"SELECT (.*?) FROM", query, re.IGNORECASE)
    from_match = re.search(r"FROM (\w+)", query, re.IGNORECASE)

    if not select_match or not from_match:
        raise ValueError("Invalid SQL query: SELECT or FROM missing")

    select_part = select_match.group(1)
    from_part = from_match.group(1)

    # WHERE
    where_match = re.search(r"WHERE (.*?) GROUP BY", query, re.IGNORECASE)
    if not where_match:
        where_match = re.search(r"WHERE (.*)", query, re.IGNORECASE)

    where_part = parse_where(where_match.group(1)) if where_match else None

    # GROUP BY
    group_match = re.search(r"GROUP BY (.*)", query, re.IGNORECASE)
    group_by_part = (
        [x.strip() for x in group_match.group(1).split(",")]
        if group_match else []
    )

    # SELECT processing
    columns, aggregations = parse_aggregations(select_part)

    return {
        "select": {
            "columns": columns,
            "aggregations": aggregations
        },
        "from": from_part,
        "where": where_part,
        "group_by": group_by_part
    }