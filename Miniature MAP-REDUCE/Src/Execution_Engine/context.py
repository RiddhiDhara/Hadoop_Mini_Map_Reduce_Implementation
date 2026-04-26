class ExecutionContext:
    def __init__(self, num_partitions=8, num_reducers=4):
        self.num_partitions = num_partitions
        self.num_reducers = num_reducers