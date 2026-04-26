def split_data(data, num_partitions):
    """
    Splits data into roughly equal partitions.
    
    :param data: List of rows
    :param num_partitions: Number of partitions to create
    :return: List of partitions
    """
    
    if num_partitions <= 0:
        raise ValueError("num_partitions must be greater than 0")
    
    total_rows = len(data)
    chunk_size = total_rows // num_partitions
    
    partitions = []
    
    for i in range(num_partitions):
        start = i * chunk_size
        
        # Last partition takes remaining rows
        if i == num_partitions - 1:
            end = total_rows
        else:
            end = (i + 1) * chunk_size
        
        partitions.append(data[start:end])
    
    return partitions