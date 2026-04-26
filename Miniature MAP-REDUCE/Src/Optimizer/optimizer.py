def build_logical_plan(query):
    return {
        "type": "AGGREGATE_QUERY",
        "operations": {
            "filter": query["where"],
            "group_by": query["group_by"],
            "aggregations": query["select"]["aggregations"]
        }
    }