# Frequent Item Counting Study

This project presents an experimental study of algorithms for identifying frequent and less frequent items in data streams, comparing exact and approximate counting approaches.

The focus is on analyzing the trade-off between accuracy, memory usage, and computational efficiency when processing large datasets.

## Implemented Algorithms

The following methods were implemented and evaluated:

- Exact Counter
- Probabilistic Counter (fixed probability: 0.125)
- Space-Saving Count Algorithm (frequent item detection)

## Key Objectives

- Compare exact and approximate counting methods
- Evaluate estimation quality using relative deviation from exact counts
- Analyze identification of the most frequent items ("heavy hitters")
- Measure computational efficiency and memory consumption
- Study scalability for large data streams

## Dataset

The analysis uses the **Portugal Real Estate 2024** dataset from Kaggle:  
https://www.kaggle.com/datasets/luvathoms/portugal-real-estate-2024

The dataset is used to apply frequency counting algorithms on the **Town** attribute, enabling evaluation of exact and approximate methods on real-world categorical data.

## Experimental Evaluation

The project includes:

- frequency distribution analysis
- relative deviation analysis
- accuracy comparison between exact and approximate methods
- heavy hitter detection quality evaluation
- runtime and memory usage comparison

## Project Structure

```text
├── study.pdf
├── data
│   ├── plots
│   └── results_csv
└── src
    ├── exact_count.py
    ├── probabilistic_count.py
    ├── space_saving.py
    └── analysis.py