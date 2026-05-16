import pandas as pd
import os
from pympler import asizeof

class SpaceSaving:
    def __init__(self, k):
        self.k = k  # number of counters
        self.counters = {}  # item -> count

    def process_item(self, item):
        if item in self.counters: # we already count this item?
            self.counters[item] += 1
        elif len(self.counters) < self.k: # we dont count it, but have free counters?
            self.counters[item] = 1
        else: # Find the item with minimum count
            min_item = min(self.counters, key=self.counters.get)
            min_count = self.counters[min_item]
            del self.counters[min_item]
            self.counters[item] = min_count + 1

    def top_items(self, n=5): # just returns top-n most frequent items
        return sorted(self.counters.items(), key=lambda x: x[1], reverse=True)[:n]



DATA_DIRECTORY = "data/portugal_listinigs.csv"
OUTPUT_DIRECTORY = "results/space_saving_counter"


if __name__ == "__main__":
    # data preprocessing
    data = pd.read_csv(DATA_DIRECTORY, usecols=["Town"])
    town_stream = data["Town"].dropna().astype(str)

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    memory_stats = [] # memory usage for each k
    for k in range(5, 2201, 5):
        ss = SpaceSaving(k)
        for town in town_stream:
            ss.process_item(town)

        top5 = ss.top_items(5) # Save top 5 items to CSV
        df_top5 = pd.DataFrame(top5, columns=["Town", "EstimatedCount"])
        csv_path = os.path.join(OUTPUT_DIRECTORY, f"space_saving_top5_{k}.csv")
        df_top5.to_csv(csv_path, index=False)

        mem_bytes = asizeof.asizeof(ss.counters) # get memory usage of all k counters
        memory_stats.append({"k": k, "memory_bytes": mem_bytes})

    mem_df = pd.DataFrame(memory_stats) # Save memory usage
    mem_csv_path = os.path.join(OUTPUT_DIRECTORY, "space_saving_memory_usage.csv")
    mem_df.to_csv(mem_csv_path, index=False)
