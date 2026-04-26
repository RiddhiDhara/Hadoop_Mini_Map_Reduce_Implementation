from Map_Reduce.splitter import split_data
from Map_Reduce.mapper import map_partition
from Map_Reduce.shuffle import shuffle
from Map_Reduce.reducer import reduce_partition
from concurrent.futures import ThreadPoolExecutor


class ExecutionEngine:

    def __init__(self, context):
        self.context = context

    def execute(self, data, query):

        # SPLIT
        partitions = split_data(data, self.context.num_partitions)

        # MAP
        with ThreadPoolExecutor(max_workers=4) as executor:
            map_results = list(executor.map(
                lambda p: map_partition(p, query),
                partitions
            ))

        # SHUFFLE
        reducer_inputs = shuffle(map_results, self.context.num_reducers)

        # REDUCE
        final_results = []

        for reducer_data in reducer_inputs:
            final_results.append(
                reduce_partition(reducer_data, query)
            )

        return final_results




