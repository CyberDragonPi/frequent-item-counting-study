import pandas
import sys
from collections import defaultdict
from pympler import asizeof
import os


DATA_DIRECTORY = "data/portugal_listinigs.csv"
OUTPUT_DIRECTORY = "results/exact_counter"

if __name__ == "__main__":
    data = pandas.read_csv(DATA_DIRECTORY) # data loading and preprocessing
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    town_stream = data["Town"].dropna().astype(str)

    exact_counter: dict[str, int] = defaultdict(int)

    for town in town_stream: # a simple exact counter with hash map
        exact_counter[town] += 1 

    # some data to compare with other approaches
    print(f"Total number of entries: {len(town_stream)}.")
    print(f"Total number of different towns: {len(exact_counter)}.")
    print(f"Total memory size {asizeof.asizeof(exact_counter)} bytes")

    dataframe_counter = pandas.DataFrame(list(exact_counter.items()), columns=["Town", "Count"])
    dataframe_counter.to_csv(os.path.join(OUTPUT_DIRECTORY, "exact_counter.csv"), index=False)

    # top 5 will be the baseline for space-saving
    top_5 = sorted(exact_counter.items(), key=lambda x: x[1], reverse=True)[:5]

    print("\nTop 5 most frequent towns:")
    for town, count in top_5:
        print(town, count)

    # in the end, each counter was stored in 28 bytes, python is weird
    size_freq = defaultdict(int)
    for v in exact_counter.values():
        size_bytes = sys.getsizeof(v)
        size_freq[size_bytes] += 1
