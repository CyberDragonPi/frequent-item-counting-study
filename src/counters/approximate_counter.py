import pandas as pd
import statistics
import random
import numpy as np
import os

from pympler import asizeof
from collections import defaultdict



# function that casts to bigger type (if possible)
def upgrade_counter(value):
    # since we start with 8bit counters, this function dinamically casts the counters for each item group, as necessary
    if isinstance(value, np.uint8): 
        return np.uint16(value) # uint8 -> uint16
    elif isinstance(value, np.uint16): 
        return np.uint32(value) # uint16 -> uint32
    else:
        return value  # cant be higher than uint32t
    

# this just stores pairs (town, freq) to csv
def store_dataframe(approximate_counter, run):
    counter_dataframe = pd.DataFrame(
        [(k, int(v)) for k, v in approximate_counter.items()],
        columns=["Town", "RawCount"]
    ).sort_values(by="RawCount", ascending=False)

    filename = os.path.join(
        OUTPUT_DIRECTORY, f"approximate_counter_run_{run:04d}.csv"
    )
    counter_dataframe.to_csv(filename, index=False)

    if run % 50 == 0:
        print(
            f"Run {run}/{N_RUNS} completed. "
            f"Unique towns: {len(approximate_counter)}"
        )
    
# this stores core memory statistics
def store_memory_statistics(memory_usage_bytes):
    memory_stats = {
        "mean_bytes": statistics.mean(memory_usage_bytes),
        "median_bytes": statistics.median(memory_usage_bytes),
        "min_bytes": min(memory_usage_bytes),
        "max_bytes": max(memory_usage_bytes),
    }

    df_memory = pd.DataFrame([memory_stats])
    df_memory["mean_kb"] = df_memory["mean_bytes"] /1024
    df_memory["median_kb"] = df_memory["median_bytes"] /1024
    df_memory["min_kb"] = df_memory["min_bytes"] /1024
    df_memory["max_kb"] = df_memory["max_bytes"] /1024

    df_memory.to_csv(
        os.path.join(OUTPUT_DIRECTORY, "memory_usage_summary.csv"),
        index=False
    )

    print("Memory usage summary saved.")

# this stores core town statistics (avg number, median, min, max...)
def store_town_statistics(n_unique_towns):
    town_stats = {
        "unique_towns_mean": statistics.mean(n_unique_towns),
        "unique_towns_median": statistics.median(n_unique_towns),
        "unique_towns_min": min(n_unique_towns),
        "unique_towns_max": max(n_unique_towns)
    }

    df_town = pd.DataFrame([town_stats])

    df_town.to_csv(
        os.path.join(OUTPUT_DIRECTORY, "town_summary.csv"),
        index=False
    )

    print("Town stats saved.")



# parameters of the experiments
P = 1/8
N_RUNS = 1000
DATA_DIRECTORY = "data/portugal_listinigs.csv"
OUTPUT_DIRECTORY = "results/dynamic_counter"


if __name__ == "__main__":
    # loading and preprocessing
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    data = pd.read_csv(DATA_DIRECTORY, usecols=["Town"])
    town_stream = data["Town"].dropna().astype(str)

    # helping arrays to store data to analyze
    memory_usage_bytes = []
    n_unique_towns = []

    for run in range(1, N_RUNS + 1):
        approximate_counter = defaultdict(lambda: np.uint8(0)) # we start with smallest data type

        for town in town_stream:
            if random.random() <= P:
                val = approximate_counter[town]

                # if neccessary, change to type with more memory
                if isinstance(val, np.uint8) and val == 255:
                    val = upgrade_counter(val)
                elif isinstance(val, np.uint16) and val == 65535:
                    val = upgrade_counter(val)

                approximate_counter[town] = val + 1 # increment

        mem_bytes = asizeof.asizeof(approximate_counter) # get memory usage
        memory_usage_bytes.append(mem_bytes)

        unique_towns = len(approximate_counter) # gte number of unique towns in this run
        n_unique_towns.append(unique_towns)

        store_dataframe(approximate_counter, run) # store counting for this run

    store_memory_statistics(memory_usage_bytes) # store statistics
    store_town_statistics(n_unique_towns)
    

